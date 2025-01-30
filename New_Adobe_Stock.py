import requests
from bs4 import BeautifulSoup
import os
import csv
import urllib.parse

def download_image(image_url, output_dir, title):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_content = response.content
            image_name = os.path.basename(image_url)
            image_path = os.path.join(output_dir, image_name)
            with open(image_path, 'wb') as f:
                f.write(image_content)
            print(f"Image downloaded: {image_path}")
        else:
            print(f"Failed to download image from: {image_url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

def extract_and_download_images(url_template, output_dir, start_page, end_page):
    output_csv = os.path.join(output_dir, 'images.csv')
    csv_header = ['Title', 'URL']
    
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_header)
            
            for page_number in range(start_page, end_page + 1):
                current_url = f"{url_template}&search_page={page_number}"
                response = requests.get(current_url)
                if response.status_code == 200:
                    html_content = response.content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    img_elements = soup.find_all('img')
                    for img_element in img_elements:
                        src_image_url = img_element.get('src')
                        lazy_image_url = img_element.get('data-lazy')
                        if src_image_url and src_image_url.endswith('.jpg'):
                            title = img_element.get('alt', '')
                            writer.writerow([title, src_image_url])
                            download_image(src_image_url, output_dir, title)
                        if lazy_image_url and lazy_image_url.endswith('.jpg'):
                            title = img_element.get('alt', '')
                            writer.writerow([title, lazy_image_url])
                            download_image(lazy_image_url, output_dir, title)
                else:
                    print(f"Failed to fetch content from {current_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
url_template = "https://stock.adobe.com/in/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfree_collection%5D=0&filters%5Bcontent_type%3Aimage%5D=1&k=stock+market&order=relevance&safe_search=1&get_facets=0&search_type=pagination"
output_directory = r"D:\istock\Adobe\test7"
start_page = 1
end_page = 3

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

extract_and_download_images(url_template, output_directory, start_page, end_page)
