import os
import requests
import json
import time
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
def download_image(url, folder_path, filename=None):
    """
    Download an image from URL to specified folder
    
    Args:
        url (str): Image URL
        folder_path (str): Destination folder path
        filename (str, optional): Custom filename. If None, uses original filename
    """
    try:
        # Create folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Send GET request
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Get filename from URL if not provided
        if filename is None:
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "downloaded_image.jpg"
        
        # Full path to save the image
        file_path = os.path.join(folder_path, filename)
        
        # Save the image
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Image downloaded successfully: {file_path}")
        return file_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def generate_image( img_prompt, folder_path, filename ):
    
    API_KEY = os.getenv("WAVESPEED_API_KEY")

    url = "https://api.wavespeed.ai/api/v3/bytedance/seedream-v3"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "enable_base64_output": False,
        "enable_sync_mode": True,
        "guidance_scale": 2.5,
        "prompt": img_prompt,
        "seed": -1,
        "size": "1080*1920"
    }

    begin = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()["data"]
        request_id = result["id"]
        print(f"Task submitted successfully. Request ID: {request_id}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return

    url = f"https://api.wavespeed.ai/api/v3/predictions/{request_id}/result"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Poll for results
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()["data"]
            status = result["status"]

            if status == "completed":
                end = time.time()
                print(f"Task completed in {end - begin} seconds.")
                url = result["outputs"][0]
                print(f"Task completed. URL: {url}")
                img_path = download_image(url, folder_path, filename)
                return img_path
            elif status == "failed":
                print(f"Task failed: {result.get('error')}")
                return None
            else:
                print(f"Task still processing. Status: {status}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

        time.sleep(0.1)
        


# if __name__ == "__main__":
#     generate_image()