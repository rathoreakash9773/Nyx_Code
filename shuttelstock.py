import requests
import csv
import os
from PIL import Image
import io

# Define constants
category = '3d-Rendered'
sub_category = 'Images' 
START_PAGE = 1
END_PAGE = 5
BASE_DIRECTORY = "/nyx_ai_data/scraping/shutterstock"

def fetch():
    # Create directories
    base_directory = os.path.join(BASE_DIRECTORY, category,sub_category)
    image_folder_name = f'{sub_category}_shutterstock_images'
    csv_file_name = f'{sub_category}_shutterstock_data.csv'
    image_directory = os.path.join(base_directory, image_folder_name)
    csv_directory = base_directory
    os.makedirs(image_directory, exist_ok=True)
    os.makedirs(csv_directory, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    # CSV file setup
    csv_file_path = os.path.join(csv_directory, csv_file_name)
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing the headers
        writer.writerow(['Image Link', 'Post Link', 'ID','Description', 'Alternate', 'Image Path'])

        image_count = 0  # To keep track of downloaded images
        for i in range(START_PAGE, END_PAGE+1):  
            url = f'https://www.shutterstock.com/_next/data/b464cd4ffc3/en/search/3d-rendered.json?page={i}&term=3d-rendered'
            
            try:
                print(f'Page {i} is scraping....')
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = response.json()
                for post in data.get('pageProps', {}).get('assets', []):
                    if 'src' in post:
                        image_response = requests.get(post['src'], headers=headers)
                        image_response.raise_for_status()
                        image = Image.open(io.BytesIO(image_response.content))
                        width, height = image.size
                        crop_box = (0, 0, width, height - 30)  # Adjust crop box if needed
                        cropped_image = image.crop(crop_box)
                        image_path = os.path.join(image_directory, f"{post['id']}.jpg")
                        cropped_image.save(image_path)
                        print(f"Downloaded and cropped {image_path}")
                        image_count += 1
                        # Write to CSV
                        writer.writerow([
                            post['id'],
                            post.get('alt', 'No text'),  # alt text
                            post.get('description', 'No description'),
                            post['src'],  # image link
                            post['link'],  # post link
                            image_path
                        ])
                    else:
                        print(f"Missing 'src' key for post {post['id']}")
            except requests.RequestException as e:
                print(f"Failed to retrieve data for page {i}: {str(e)}")

    # Print summary at the end
    print(f"Downloaded {image_count} images.")
    print(f"CSV created at: {csv_file_path}")

fetch()
