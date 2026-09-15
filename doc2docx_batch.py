import os
import glob
import subprocess

def batch_convert_doc_to_docx(folder_path):
    """
    Scans a folder for all .doc files on macOS and converts them 
    to .docx using LibreOffice to preserve visual structure.
    """
    # Default installation path for LibreOffice on macOS
    soffice_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    
    if not os.path.exists(soffice_path):
        print("Error: LibreOffice is not installed in /Applications/")
        print("Please run: brew install --cask libreoffice")
        return

    # Expand user paths (like ~/Documents) and get absolute path
    absolute_folder = os.path.abspath(os.path.expanduser(folder_path))
    
    if not os.path.isdir(absolute_folder):
        print(f"Error: The directory '{absolute_folder}' does not exist.")
        return

    # Find all .doc files (ignoring case, matching .doc but NOT .docx)
    # We use a specific pattern filter to make sure .docx files aren't picked up
    all_files = glob.glob(os.path.join(absolute_folder, "*"))
    doc_files = [f for f in all_files if f.lower().endswith('.doc')]

    if not doc_files:
        print(f"No .doc files found in: {absolute_folder}")
        return

    print(f"Found {len(doc_files)} '.doc' file(s) to convert.\n")

    # Loop through each file and convert it
    for index, doc_path in enumerate(doc_files, 1):
        filename = os.path.basename(doc_path)
        print(f"[{index}/{len(doc_files)}] Converting: {filename}...")
        
        try:
            # Run the headless conversion command
            subprocess.run([
                soffice_path,
                "--headless",
                "--convert-to", "docx",
                doc_path,
                "--outdir", absolute_folder
            ], capture_output=True, text=True, check=True)
            
            print(f" -> Success!")
            
        except subprocess.CalledProcessError as e:
            print(f" -> Failed to convert {filename}. Error:\n{e.stderr}")

    print("\nBatch conversion complete!")

# Example Usage:
# Replace with the path to your folder (e.g., "~/Documents/my_word_files")
target_folder = "./"
batch_convert_doc_to_docx(target_folder)
