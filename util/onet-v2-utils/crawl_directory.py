import os
import json
import argparse
from docx import Document
import subprocess


def crawl_directory(foldername):
    # Check if the folder exists
    if not os.path.exists(foldername):
        print(f"The folder {foldername} does not exist.")
        return

    # Extract all files with their modification times
    all_files = {
        file: os.path.getmtime(os.path.join(foldername, file))
        for file in os.listdir(foldername)
        if os.path.isfile(os.path.join(foldername, file))
    }

    # Sort the files by modification time
    sorted_files = sorted(all_files.items(), key=lambda x: x[1])

    # Using a set to keep track of base filenames already processed
    processed = set()
    unique_files = []

    for file, _ in sorted_files:
        base_name = os.path.splitext(file)[0]
        if base_name not in processed:
            unique_files.append(base_name)
            processed.add(base_name)

    # Prepare the data for JSON export
    filenames_json = [{"filename": filename} for filename in unique_files]

    return filenames_json


def create_blank_txt_files(filenames):
    text_dir = "./text"
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)

    for entry in filenames:
        filename = entry["filename"]
        with open(os.path.join(text_dir, f"{filename}.txt"), "w") as file:
            pass  # Creating a blank file


def convert_doc_to_txt(foldername):
    text_dir = "./text"
    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            base_name = os.path.splitext(filename)[0]
            doc_path = os.path.join(foldername, f"{base_name}.doc")
            if os.path.exists(doc_path):
                try:
                    # Use LibreOffice to convert .doc to .txt
                    subprocess.run(
                        [
                            "libreoffice",
                            "--headless",
                            "--convert-to",
                            "txt:Text",
                            "--outdir",
                            foldername,
                            doc_path,
                        ]
                    )
                    txt_converted_path = os.path.join(foldername, f"{base_name}.txt")
                    if os.path.exists(txt_converted_path):
                        with open(txt_converted_path, "r") as src_file:
                            content = src_file.read()
                        with open(os.path.join(text_dir, filename), "w") as dest_file:
                            dest_file.write(content)
                        # Optionally, remove the intermediate .txt file
                        os.remove(txt_converted_path)
                except Exception as e:
                    print(f"Error converting {doc_path} to .txt: {e}")


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description="Crawl a directory and create a JSON file of unique filenames."
    )
    parser.add_argument("foldername", help="The folder to crawl.")
    args = parser.parse_args()

    # Crawl the directory
    data = crawl_directory(args.foldername)
    if data:
        # Write the data to directory.json
        with open("directory.json", "w") as file:
            json.dump(data, file, indent=4)

        # Create blank .txt files for each filename in /text
        create_blank_txt_files(data)
        convert_doc_to_txt(args.foldername)


if __name__ == "__main__":
    main()
