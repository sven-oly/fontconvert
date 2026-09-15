import subprocess
import os

soffic_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

def convert_with_libreoffice(doc_path, output_dir="."):
    try:
        # Call LibreOffice headless converter
        subprocess.run([
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',
            '--headless', 
            '--convert-to', 'docx', 
            doc_path, 
            '--outdir', output_dir
        ], check=True)
        print("Conversion complete!")
    except FileNotFoundError:
        print("Error: LibreOffice 'soffice' command not found. Please install LibreOffice.")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")

# Example usage
convert_with_libreoffice("test_data/phk_docx/TEST_doc.doc")
