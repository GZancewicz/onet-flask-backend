import os
from bs4 import BeautifulSoup
import sys

# Open and parse the template.html
with open("template.html", "r") as file:
    template_content = file.read()

# Walk through ../content and its subdirectories
for dirpath, dirnames, filenames in os.walk("../content"):
    for filename in filenames:
        # Process only .html files
        if filename.endswith(".html") and not filename.startswith("_"):
            # Construct the full file path
            filepath = os.path.join(dirpath, filename)

            # Open and parse the HTML file
            print(filepath)
            with open(filepath, "r", encoding="utf-8") as file:
                infile_content = file.read()
            infile_soup = BeautifulSoup(infile_content, "html.parser")

            # Extract the contents of <div id="page-content"> from infile as a string
            page_content_infile = infile_soup.find("div", {"id": "page-content"})
            if page_content_infile is None:
                print(f"No element with id 'page-content' found in {filepath}")
                continue
            page_content_infile_str = str(page_content_infile)

            # Replace the placeholder div with this string in template_content
            template_content_modified = template_content.replace(
                '<div id="placeholder"></div>', page_content_infile_str
            )

            # Write the modified template content back to infile
            with open(filepath, "w") as file:
                file.write(template_content_modified)
