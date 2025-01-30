import requests
import csv
import os

zone = 'south'
state = 'kerala'
city = 'mattencherry'
link = 'link1'
start_page = 11
end_page = 11
def fetch(end_page):
    # create directories
    base_directory = r"\nyx_ai_data\ai_dev\{zone}\{state}\{city}\link1".format(zone=zone, state=state, city=city)
    image_folder_name = f'{city}_shutterstock_images'
    csv_file_name = f'{city}_shutterstock_data.csv'
    image_directory = os.path.join(base_directory, image_folder_name)
    csv_directory = base_directory  # You can change this if you prefer a different directory for the CSV
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
        for i in range(start_page, end_page):  # Assuming you might want to loop through pages
            url = f'https://www.shutterstock.com/_next/data/fe8a0a0a8b9/en/_shutterstock/search/thanjavur.json?image_type=photo&page={i}&term=thanjavur'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    data = response.json()
                    for post in data['pageProps']['assets']:
                        if 'src' in post :
                            image_response = requests.get(post['src'], headers=headers)
                            if image_response.status_code == 200:
                                image_path = os.path.join(image_directory, f"{post['id']}.jpg")
                                with open(image_path, 'wb') as img_file:
                                    img_file.write(image_response.content)
                                print(f"Downloaded {image_path}")
                                image_count += 1
                                # Write to CSV
                                writer.writerow([
                                    post['id'],
                                    post.get('alt','No text'), # alt text
                                    post.get('description','No description'),
                                    post['src'],  # image link
                                    post['link'],  # post link
                                    image_path
                                ])
                            else:
                                print(f"Failed to download image for post {post['id']}")
                        else:
                            print(f"Missing 'src' key for post {post['id']}")
                except ValueError:
                    print("Response is not in JSON format")
            else:
                print(f"Failed to retrieve data for page {i}, status code:", response.status_code)

    # Print summary at the end
    print(f"Downloaded {image_count} images.")
    print(f"CSV created at: {csv_file_path}")

start_page = 11
end_page = 11
fetch(end_page+1)
