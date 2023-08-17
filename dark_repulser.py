import os
import hashlib
import urllib.parse
import datetime
from tqdm import tqdm
import time
from common_functions import download_image, cache_directory, cached_paths_file, get_path_hash, deduplicate_cached_paths

def update_cache():
    # Run the deduplication function
    deduplicate_cached_paths()
    # Read the cached paths from the file
    cached_paths = []
    with open(cached_paths_file, 'r') as file:
        cached_paths = [line.strip() for line in file.readlines()]

    # Iterate over the cached paths and update the cache
    for path in tqdm(cached_paths):
        # print(path)
        # Generate the SHA256 hash of the path
        path_hash = get_path_hash(path)

        # Get the file extension from the path
        parsed_url = urllib.parse.urlparse(path)
        _, file_extension = os.path.splitext(parsed_url.path)
        file_extension = file_extension.lower()  # Convert to lowercase for consistency

        # Construct the cached image path with the file extension
        cached_image_path = os.path.join(cache_directory, f"{path_hash}{file_extension}")

        # Download the image and save it to the cache no matter what
        download_image(path, cached_image_path)

def main():
    update_cache()
    while True:
        # Get the current time
        now = datetime.datetime.now().time()

        # Set the target time to 7am
        target_time = datetime.time(7, 0, 0)

        # Check if debug mode is enabled
        debug = False

        # If debug mode is enabled, set target_time to 2 minutes from now
        if debug:
            current_datetime = datetime.datetime.now()
            target_time = datetime.time(current_datetime.hour, current_datetime.minute + 2, current_datetime.second)
            print("Trig on", current_datetime.hour, current_datetime.minute + 2, current_datetime.second)

        # Calculate the time difference between now and 7am
        time_difference = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), now)

        # Check if we are currently before 7am
        is_before_7am = time_difference.total_seconds() > 0

        # Initialize the previous boolean values
        prev_is_before_7am = is_before_7am

        # Loop until it's no longer before 7am and the previous boolean was True
        while not (prev_is_before_7am and not is_before_7am):
            # Sleep for 10 seconds
            time.sleep(10)
            
            # Update the current time
            now = datetime.datetime.now().time()
            
            # Recalculate the time difference
            time_difference = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), now)
            print(time_difference)
            # Update the boolean values
            prev_is_before_7am = is_before_7am
            is_before_7am = time_difference.total_seconds() > 0
            print(prev_is_before_7am, is_before_7am)

        # Run the update cache function
        update_cache()

if __name__ == "__main__":
    main()