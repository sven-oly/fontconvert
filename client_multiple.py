import time
import requests

SERVER_URL = "https://appspot.com"  # Replace with your deployed URL

# 1. Define files to upload
files_to_send = [
    ('files', ('doc1.txt', b'hello world from file one')),
    ('files', ('doc2.txt', b'apple banana orange cherry'))
]

# 2. Upload files
print("Uploading files...")
response = requests.post(f"{SERVER_URL}/upload", files=files_to_send)
data = response.json()
print(data["message"])

# 3. Wait for background Cloud Tasks to complete processing
print("Waiting for processing to complete...")
time.sleep(5)

# 4. Download processed files
for file_id, original_info in zip(data["task_ids"], files_to_send):
    filename = original_info[1][0]
    download_url = f"{SERVER_URL}/download/{file_id}/{filename}"

    print(f"Downloading {filename}...")
    dl_response = requests.get(download_url)

    if dl_response.status_code == 200:
        with open(f"processed_{filename}", "wb") as f:
            f.write(dl_response.content)
        print(f"Saved processed_{filename}")
    else:
        print(f"Failed to download {filename}: {dl_response.text}")
