import sys
from PIL import Image

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py filename.png")
    sys.exit(1)

# Get the input filename from the command-line argument
input_filename = sys.argv[1]

# Check if the input filename has the correct extension
if not input_filename.endswith('.png'):
    print("Please provide a PNG file.")
    sys.exit(1)

# Open the PNG image
image = Image.open(input_filename)

# Construct the output filename by replacing the extension
output_filename = input_filename[:-4] + '.webp'

# Convert and save the image in WebP format
image.save(output_filename, "WEBP")

print(f"Converted {input_filename} to {output_filename}")
