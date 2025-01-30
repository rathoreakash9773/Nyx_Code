import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import hashlib
import csv

def download_images(url, base_dir, num_pages,output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    img_folder = os.path.join(base_dir,output_folder)

    # Create a list to store image information
    image_info_list = []

    # Add headers to mimic a regular browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page_num in range(1, num_pages + 1):
        page_url = f"{url}&page_num={page_num}"
        print(f"Downloading images from page {page_num}...")

        try:
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page_num}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        image_tags = soup.find_all('img')

        for img_tag in image_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(url, img_url)
                img_name = hashlib.sha1(img_url.encode()).hexdigest()[:10]  # Generate a unique filename
                img_path = os.path.join(img_folder, img_name + ".jpg")  # Ensure the image has a .jpg extension

                try:
                    with open(img_path, 'wb') as img_file:
                        img_response = requests.get(img_url, headers=headers)
                        img_response.raise_for_status()  # Raise an exception for bad responses
                        img_file.write(img_response.content)

                    # Collect image information
                    image_info = {
                        'ID': img_name,
                        'URL': img_url,
                        'Title': img_tag.get('title', ''),
                        'Image path': img_path
                    }
                    image_info_list.append(image_info)
                except requests.exceptions.RequestException as e:
                    print(f"Failed to download image from {img_url}: {e}")
                    continue

        # Add a delay between requests to avoid rate-limiting
        time.sleep(1)

    # Write image information to a CSV file
    csv_file_path = os.path.join(base_dir, f'{output_folder}.csv')
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['ID', 'URL', 'Title', 'Image path']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for image_info in image_info_list:
            writer.writerow(image_info)

    print("CSV file created successfully!")

if __name__ == "__main__":
    url = "https://freerangestock.com/search.php?search=animal&orderby=views30&match_type=all&gid_search=&gid=&startat=100&perpage=50&type=all"
    base_dir = r'C:/File Manager/NYX Work/Freerange'
    category = 'animal'
    output_folder = f"{category}_freerange_images"
    num_pages = 2

    download_images(url, base_dir, num_pages,output_folder)