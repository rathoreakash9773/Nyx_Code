#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import csv
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

category = 'Vehicle'
base_directory = r"C:\Users\areeb\Downloads\hehe"
image_folder_name = f"{category}_lifeofpix_images"
csv_file_path = f"{category}_lifeofpix_data.csv"
images_directory = os.path.join(base_directory, image_folder_name)
csv_file_directory = os.path.join(base_directory, csv_file_path)
os.makedirs(images_directory, exist_ok=True)

try:
    with open(csv_file_directory, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Filename', 'Seo Title', 'Size', 'Width', 'Height', 'Date Updated', 'Accent Color', 'URL Download', 'Uploader ID', 'Uploader Fullname', 'Uploader Username', 'Uploader City', 'Uploader Country', 'Uploader Instagram Handle', 'Uploader Website'])

        page_num = 1
        image_counter = 1  # Counter for sequential numbering
        downloaded_ids = set()  # Set to store downloaded photo IDs

        while True:
            url = f'https://www.lifeofpix.com/api/gallery/{category}/20/{page_num}.json'
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            if not data['photos']:
                break  # No more photos, exit the loop

            for photo in data['photos']:
                try:
                    # Extract photo information
                    photo_id = photo['id']

                    # Check if photo ID is already downloaded, skip if it is
                    if photo_id in downloaded_ids:
                        continue

                    filename = photo['filename']
                    seo_title = photo['seoTitle']
                    size = photo['size']
                    width = photo['width']
                    height = photo['height']
                    date_updated = photo['dateUpdated']
                    accent_color = photo['accentColor']
                    url_download = photo['urlDownload']

                    # Extract uploader information
                    uploader = photo['uploader']
                    uploader_id = uploader['id']
                    uploader_fullname = uploader['fullname']
                    uploader_username = uploader['username']
                    uploader_city = uploader['userCity']
                    uploader_country = uploader['userCountry']
                    uploader_instagram_handle = uploader['userInstagramHandle']
                    uploader_website = uploader['userWebsite']

                    # Replace problematic characters in the image name and include counter
                    image_name = f"{image_counter}_{seo_title.replace('|', '_')}"
                    image_counter += 1

                    # Write to CSV
                    writer.writerow([
                        photo_id, filename, seo_title, size, width, height, date_updated, accent_color, url_download,
                        uploader_id, uploader_fullname, uploader_username, uploader_city, uploader_country,
                        uploader_instagram_handle, uploader_website
                    ])

                    # Download image
                    image_url = photo['url']
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    image_path = os.path.join(images_directory, f"{image_name}.jpg")
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)
                        print('Image downloaded:', image_path)

                    # Add the downloaded photo ID to the set
                    downloaded_ids.add(photo_id)

                except requests.exceptions.RequestException as e:
                    print(f"Failed to download image for photo {photo_id}: {e}")
                except Exception as e:
                    print(f"Unexpected error while processing photo {photo_id}: {e}")

            page_num += 20  # Increment the page number by 20 for the next iteration

except IOError as e:
    print(f"Error opening/writing to CSV file: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

print('CSV file saved at:', csv_file_directory)

