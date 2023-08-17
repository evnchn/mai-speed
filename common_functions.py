from PIL import Image
import requests
import os
import hashlib

# Define the cache directory where images will be stored
cache_directory = os.path.join(os.getcwd(), 'cache')

# Define the path to the file storing cached paths
cached_paths_file = os.path.join(os.getcwd(), 'cached_paths.txt')

def get_path_hash(path):
    path_hash = hashlib.sha256(path.encode()).hexdigest()
    return path_hash

def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            # The file is a valid image
            return True
    except (IOError, OSError):
        # The file is not a valid image
        return False
    

def download_image(url, destination):
    return_val = 0
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Check the content type of the response
        content_type = response.headers.get('Content-Type')
        if content_type and content_type.startswith('image'):
            with open(destination, 'wb') as file:
                file.write(response.content)
                return_val = len(response.content)

            # Check if the downloaded file is a valid image
            if not is_image(destination):
                os.remove(destination)
                print(f"Downloaded file is not a valid image: {url}")
        else:
            print(f"Invalid content type: {content_type}. Expected an image.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
    return return_val

def deduplicate_cached_paths():
    # Read the contents of the file into a list
    with open(cached_paths_file, 'r') as file:
        cached_paths = file.readlines()

    # Remove duplicates while preserving the order
    deduplicated_paths = list(dict.fromkeys(cached_paths))

    # Write the deduplicated paths back to the file
    with open(cached_paths_file, 'w') as file:
        file.writelines(deduplicated_paths)