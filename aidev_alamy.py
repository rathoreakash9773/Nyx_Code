import requests
import csv
import os

zone = 'south'
state = 'kerala'
city = 'mattencherry'
link = 'link1'
start_page = 1
end_page = 100
def fetch(end_page):
    # Base directory path where you want to save everything
    base_directory = r"/nyx_ai_data/ai_dev/{zone}/{state}/{city}/link1".format(zone=zone, state=state, city=city)
    image_folder_name = f'{link}_{city}_alamy_images'
    csv_file_name = f'{link}_{city}_alamy_data.csv'
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
        writer.writerow(['URL', 'Caption', 'Upload Date', 'ID', 'Image Path'])

        image_count = 0  # To keep track of downloaded images
        for i in range(start_page, end_page):  # Assuming you might want to loop through pages
            url = f'https://www.alamy.com/search-api/search/?qt=udaipur&imgt=1&hc=1,2,3,4,5%2B&sortBy=relevant&collectiontype=all-creative&ispartial=true&langcode=en&isbot=false&type=picture&geo=IN&pn={i}&ps=50&nasty=0&editorial=1&rmuid=31114ba7-0b90-42fa-afb9-841b51127a18&translate=true&sessionid=31114ba7-0b90-42fa-afb9-841b51127a18'
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    data = response.json()
                    for post in data['items']:
                        # Ensure 'renditions' and 'zoom_large' keys exist
                        if 'renditions' in post and 'zoom_large' in post['renditions']:
                            image_response = requests.get(post['renditions']['zoom_large']['href'], headers=headers)
                            if image_response.status_code == 200:
                                image_path = os.path.join(image_directory, f"{post['altids']['seq']}.jpg")
                                with open(image_path, 'wb') as img_file:
                                    img_file.write(image_response.content)
                                print(f"Downloaded {image_path}")
                                image_count += 1
                                # Write to CSV
                                writer.writerow([
                                    post['renditions']['zoom_large']['href'],
                                    post.get('caption', 'No caption'),  # Safely get 'caption' or default to 'No caption'
                                    post['uploaddate'].split('T')[0],
                                    post['altids']['seq'],
                                    image_path
                                ])
                            else:
                                print(f"Failed to download image for post {post['id']}")
                        else:
                            print(f"Missing 'renditions' or 'zoom_large' key for post {post['id']}")
                except ValueError:
                    print("Response is not in JSON format")
            else:
                print(f"Failed to retrieve data for page {i}, status code:", response.status_code)

    # Print summary at the end
    print(f"Downloaded {image_count} images.")
    print(f"CSV created at: {csv_file_path}")

fetch()
