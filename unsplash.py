import requests
import csv
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}


category = 'film'
base_directory = r"/nyx_ai_data/scraping/unsplash"
image_folder_name = f"{category}_unsplash_images"
csv_file_path = f"{category}_unsplash_data.csv"
images_directory = os.path.join(base_directory, image_folder_name)
csv_file_directory = os.path.join(base_directory, csv_file_path)
os.makedirs(images_directory, exist_ok=True)

try:
    with open(csv_file_directory, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Writing the headers
        writer.writerow(['ID', 'Updated At', 'Description', 'Likes', 'Raw URL', 'Image Path'])

        for i in range(1, 100):
            url = f'https://unsplash.com/napi/topics/{category}/photos?page=8&per_page=30'
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # This will raise an exception for 4xx/5xx errors
                data = response.json()
                # Inside the loop where you process each post
                for post in data:
                    try:
                        # Initialize variables to store post data, providing default values in case of exceptions
                        post_id = post_updated_at = post_description = post_likes = post_raw_url = "Not Available"
                        # Attempt to extract each piece of data with error handling
                        try:
                            post_id = post['id']
                        except KeyError:
                            print("ID not found for a post, defaulting to 'Not Available'")
                        try:
                            post_updated_at = post['updated_at']
                        except KeyError:
                            print("Updated At not found for post ID:", post_id)
                        try:
                            post_description = post['description'] if post['description'] else "No description"
                        except KeyError:
                            print("Description not found for post ID:", post_id)
                        try:
                            post_likes = post['likes'] if post['likes'] else "Not Found"
                        except KeyError:
                            print("Likes not found for post ID:", post_id)
                        try:
                            post_raw_url = post['urls']['raw']
                        except KeyError:
                            print("Raw URL not found for post ID:", post_id)
                        # If all goes well, proceed to download image and write to CSV
                        image_response = requests.get(post_raw_url)
                        image_response.raise_for_status()  # This will raise an exception for HTTP errors
                        image_path = os.path.join(images_directory, f"{post_id}.jpg")
                        with open(image_path, 'wb') as img_file:
                            img_file.write(image_response.content)
                            print('Image downloaded:', image_path)
                        # Writing to the CSV
                        writer.writerow([
                            post_id,
                            post_updated_at,
                            post_description,
                            post_likes,
                            post_raw_url,
                            image_path 
                        ])
                        print('csv created',csv_file_path)
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to download image for post {post_id}: {e}")
                    except Exception as e:
                        print(f"Unexpected error while processing post {post_id}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve data for page {i}: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")


except IOError as e:
    print(f"Error opening/writing to CSV file: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
print('CSV file saved at:', csv_file_directory)