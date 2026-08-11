import os
import uuid
from flask import Flask, request, jsonify, send_file
from google.cloud import storage
from google.cloud import tasks_v2

app = Flask(__name__)

# Configuration (Replace with your actual values)
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
QUEUE_ID = "file-processing-queue"
BUCKET_NAME = "your-app-file-bucket"  # Unified bucket for input/output

# Initialize GCP Clients
storage_client = storage.Client()
tasks_client = tasks_v2.CloudTasksClient()
bucket = storage_client.bucket(BUCKET_NAME)


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    if not uploaded_files:
        return "No files provided", 400

    task_ids = []

    for file in uploaded_files:
        # 1. Generate unique IDs to prevent filename collisions
        file_uuid = str(uuid.uuid4())
        input_gcs_path = f"raw/{file_uuid}_{file.filename}"
        output_gcs_path = f"processed/{file_uuid}_{file.filename}"

        # 2. Upload raw file to Cloud Storage
        blob = bucket.blob(input_gcs_path)
        blob.upload_from_file(file)

        # 3. Construct Cloud Task Payload (Keep it under 100KB)
        # Pass GCS references instead of raw binary data
        payload = {
            "input_path": input_gcs_path,
            "output_path": output_gcs_path,
            "filename": file.filename
        }

        # 4. Create the Cloud Task
        queue_path = tasks_client.queue_path(PROJECT_ID, LOCATION, QUEUE_ID)
        # Point the task to your app's /worker endpoint (App Engine URL or Cloud Run URL)
        task_url = f"https://{PROJECT_ID}://"

        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": task_url,
                "headers": {"Content-Type": "application/json"},
                "body": jsonify(payload).data
            }
        }

        tasks_client.create_task(parent=queue_path, task=task)
        task_ids.append(file_uuid)

    # Return the unique IDs so the client knows what to poll/download later
    return jsonify({"message": f"Enqueued {len(task_ids)} files", "task_ids": task_ids}), 200


@app.route('/worker', methods=['POST'])
def worker_process():
    """Cloud Tasks Worker Target."""
    data = request.get_json()
    input_path = data['input_path']
    output_path = data['output_path']

    # 1. Download file from GCS into worker memory
    input_blob = bucket.blob(input_path)
    file_bytes = input_blob.download_as_bytes()

    # 2. Process the file (Example: Convert text to uppercase)
    processed_bytes = file_bytes.upper()

    # 3. Upload the processed file back to GCS
    output_blob = bucket.blob(output_path)
    output_blob.upload_from_string(processed_bytes)

    # 4. Clean up raw file from GCS to save space (Optional)
    input_blob.delete()

    return "Processing complete", 200


@app.route('/download/<file_id>/<filename>', methods=['GET'])
def download_file(file_id, filename):
    """Serves the processed file back to the client."""
    output_gcs_path = f"processed/{file_id}_{filename}"
    blob = bucket.blob(output_gcs_path)

    if not blob.exists():
        return "File is still processing or does not exist", 404

    # Download file to local memory and stream to client
    file_data = blob.download_as_bytes()

    # Optional: Delete from GCS after successful delivery to save storage costs
    # blob.delete()

    from io import BytesIO
    return send_file(
        BytesIO(file_data),
        download_name=f"processed_{filename}",
        as_attachment=True
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

3.
Queue
Configuration(queue.yaml)

queue:
- name: file - processing - queue
rate: 5 / s
max_concurrent_requests: 10
retry_parameters:
task_retry_limit: 5
