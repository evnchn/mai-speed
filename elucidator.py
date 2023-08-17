import os
import hashlib
from flask import Flask, request, send_from_directory, redirect
import urllib.parse
from common_functions import download_image, cache_directory, cached_paths_file, get_path_hash, deduplicate_cached_paths
import datetime

app = Flask(__name__)

@app.route("/am_i_ok")
def i_am_ok():
    return "I am OK"

@app.route("/<path:path>")
def cache_photo(path):
    path = f"https://{path}"
    # path = request.args.get("path")
    path = path.strip()

    # Verify the domain of the URL
    parsed_url = urllib.parse.urlparse(path)
    if parsed_url.netloc != 'maimaidx-eng.com':
        print(f"Invalid URL domain: {path}")
        print(parsed_url.netloc)
        # Redirect the client to fetch the image themselves
        return redirect(path)

    if not path:
        return "Path parameter is missing", 400

    # Generate the SHA256 hash of the path
    path_hash = get_path_hash(path)
    
    # Get the file extension from the path
    _, file_extension = os.path.splitext(parsed_url.path)
    file_extension = file_extension.lower()  # Convert to lowercase for consistency

    # Create the cache directory if it doesn't exist
    try:
        os.makedirs(cache_directory)
    except:
        pass

    # Construct the cached image path with the file extension
    cached_image_path = os.path.join(cache_directory, f"{path_hash}{file_extension}")

    # Check if the image is already cached
    if not os.path.exists(cached_image_path):
        # Download the image and save it to the cache
        download_image(path, cached_image_path)

    # Set caching headers to maximize caching settings
    response = send_from_directory(cache_directory, f"{path_hash}{file_extension}")
    #response.headers['Cache-Control'] = 'public, max-age=10800'  # Cache for 3 hour, duration of server maintenance
    #expires_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=10800)
    #response.headers['Expires'] = expires_time.strftime('%a, %d %b %Y %H:%M:%S GMT')# Cache for 3 hour, duration of server maintenance
    
    response.cache_control.no_cache = None
    # response.cache_control.private = False
    response.cache_control.max_age = 10800
    response.cache_control.public = True
    response.headers['Cache-Control'] = 'public, immutable, max-age=3600, stale-while-revalidate=600, stale-if-error=259200'
    print("->",response.headers['Cache-Control'])
    print("--->", response.cache_control)

    # Server maintenance 3-6am
    # Shops open at early as 8am
    # Cache updated at 7am, perfect

    # Store the cached path in the file
    store_cached_path(path)

    return response

counter = 0
def store_cached_path(path):
    global counter
    with open(cached_paths_file, 'a') as file:
        file.write(path + '\n')
        counter += 1
        print("Deduplication counter", counter)
        if counter > 1000: # every N loads or so, one lag spike may occur
            deduplicate_cached_paths()
            counter = 0
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)