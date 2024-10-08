import re
import os
import requests

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the XLIFF folder to the script's directory
xliff_folder = script_dir

# Directory to save images (inside the script's directory)
download_dir = os.path.join(script_dir, "screenshots")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Function to process each XLIFF file
def process_xliff_file(file_path):
    # Open and read the XLIFF file
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()
    
    # Extract all screenshot links
    links = re.findall(r'<context context-type="x-screenshots">(https?://\S+)</context>', xml_data)
    
    # Download each screenshot
    for idx, link in enumerate(links, start=1):
        try:
            # Get the image
            response = requests.get(link)
            response.raise_for_status()  # Ensure the request was successful
            
            # Determine image file name (using .jpg as the extension)
            file_name = os.path.join(download_dir, f"screenshot_{os.path.basename(file_path)}_{idx}.jpg")
            
            # Save the image
            with open(file_name, 'wb') as file:
                file.write(response.content)
            
            print(f"Downloaded: {file_name}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {link}: {e}")

# Get all XLIFF files in the script's directory
for file_name in os.listdir(xliff_folder):
    if file_name.endswith('.xliff'):
        file_path = os.path.join(xliff_folder, file_name)
        print(f"Processing file: {file_path}")
        process_xliff_file(file_path)
