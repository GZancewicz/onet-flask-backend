import sys
from bs4 import BeautifulSoup


def extract_body_content(input_html_file, output_html_file):
    # Open and read the input HTML file
    with open(input_html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Extract the content inside the <body> tag
    body_content = soup.body.prettify()

    # Write the content to the output file
    with open(output_html_file, "w", encoding="utf-8") as file:
        file.write(body_content)


if __name__ == "__main__":
    # Check if the user provided the input file name
    if len(sys.argv) < 2:
        print("Usage: python strip_body.py <input_html_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "output.html"  # Default output file name

    # If the user provided an output file name, use it
    if len(sys.argv) == 3:
        output_file = sys.argv[2]

    extract_body_content(input_file, output_file)
