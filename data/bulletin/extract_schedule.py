
import sys
import re
import json
from pathlib import Path
from pdfminer.high_level import extract_text

def pdf_to_text_pdfminer(pdf_path):
    return extract_text(pdf_path)

def parse_file(txt_content):
    # Splitting the content based on blank lines to get individual sections
    sections = [section.strip() for section in txt_content.split('\n\n') if section.strip()]
    
    # Extracting times, dates and services
    times = sections[3].split('\n')
    dates = sections[4].split('\n')
    services = sections[5].split('\n')
    
    # Combining times, dates, and services
    combined_data = []
    for i in range(len(dates)):
        entry = {
            "date": dates[i],
            "time": times[i] if i < len(times) else None,
            "service": services[i] if i < len(services) else None
        }
        combined_data.append(entry)

    # Filtering out entries that don't have "date" formatted like "Day m/dd"
    filtered_data = [entry for entry in combined_data if re.match(r'^[A-Za-z]{3} \d{1,2}/\d{2}$', entry["date"].strip())]
    
    return filtered_data

def main():
    # Check if the argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py /path/to/pdf_file.pdf")
        sys.exit(1)

    # Convert the PDF to text
    pdf_path = sys.argv[1]
    txt_content = pdf_to_text_pdfminer(pdf_path)

    # Parse the text content
    parsed_data = parse_file(txt_content)
    
    # Save the data to schedule.json
    with open("schedule.json", "w") as f:
        json.dump(parsed_data, f, indent=4)

    print("Data saved to schedule.json")

if __name__ == "__main__":
    main()
