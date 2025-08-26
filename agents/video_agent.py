import os
import requests
import json
import time
from urllib.parse import urlparse
from dotenv import load_dotenv
import ffmpeg

load_dotenv()
def download_video(url, folder_path, filename):
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

def generate_video(video_prompt, image_url, folder_path, filename):
    
    API_KEY = os.getenv("WAVESPEED_API_KEY")

    url = "https://api.wavespeed.ai/api/v3/wavespeed-ai/wan-2.2/i2v-5b-720p"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "image": image_url,
        "prompt": video_prompt,
        "seed": -1
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
                vid_url = result["outputs"][0]
                print(f"Task completed. URL: {vid_url}")
                vid_path = download_video(vid_url, folder_path, filename)
                return vid_url, vid_path
            elif status == "failed":
                print(f"Task failed: {result.get('error')}")
                return None
            else:
                print(f"Task still processing. Status: {status}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

        time.sleep(0.1)

def generate_video_waudio(audio_prompt, video_url, folder_path, filename):
    
    API_KEY = os.getenv("WAVESPEED_API_KEY")

    url = "https://api.wavespeed.ai/api/v3/wavespeed-ai/mmaudio-v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "duration": 5,
        "guidance_scale": 4.5,
        "mask_away_clip": False,
        "negative_prompt": "",
        "num_inference_steps": 25,
        "prompt": audio_prompt ,
        "video": video_url
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
                vid_url = result["outputs"][0]
                print(f"Task completed. URL: {url}")
                vid_path = download_video(vid_url, folder_path, filename)
                return vid_url, vid_path
            elif status == "failed":
                print(f"Task failed: {result.get('error')}")
                return None
            else:
                print(f"Task still processing. Status: {status}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
        time.sleep(0.1)

def join_mp4_files(input_files, output_file):
    """
    Join videos using FFmpeg concat demuxer (fastest method)
    """
    try:
        # Create temporary file list
        list_file = "file_list.txt"
        
        with open(list_file, 'w') as f:
            for file in input_files:
                f.write(f"file '{os.path.abspath(file)}'\n")
        
        # Use concat demuxer
        (
            ffmpeg
            .input(list_file, format='concat', safe=0)
            .output(output_file, c='copy')
            .overwrite_output()
            .run()
        )
        
        print(f"Successfully joined videos to: {output_file}")
        return True
        
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        # Clean up temporary file
        if os.path.exists(list_file):
            os.remove(list_file)


# if __name__ == "__main__":
#     generate_image()