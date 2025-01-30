import csv
import os
import requests
from urllib.parse import urlparse

# Path to the CSV file containing image URLs
csv_file_path = 'artstation.csv'  # scrape csv  input

# Directory to save downloaded images
download_directory = 'Artstation'  # output directory

# Create the download directory if it doesn't exist
os.makedirs(download_directory, exist_ok=True)

# Function to download an image from a URL
def download_image(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Open the CSV file and download images
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        image_url = row[0]
        file_name = os.path.basename(urlparse(image_url).path)
        file_name = file_name.split("?")[0]  # Remove URL parameters from the file name
        file_path = os.path.join(download_directory, file_name)
        if not os.path.exists(file_path):
            download_image(image_url, file_path)
        else:
            print(f"Skipping already downloaded image: {file_name}")
