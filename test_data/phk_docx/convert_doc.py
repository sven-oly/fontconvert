import subprocess

def convert_with_textutil(doc_path, output_path):
    try:
        # textutil is built into macOS
        subprocess.run(["textutil", "-convert", "docx", doc_path, "-output", output_path], check=True)
        print(f"Successfully converted to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")

# Example usage
convert_with_textutil("TEST_doc.doc", "TEST_doc.docx")
