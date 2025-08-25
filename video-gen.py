
import json
import pprint
import os
from agents.video_agent import generate_video, join_mp4_files
project_num = 6
def main():
    #load_json
    def load_json(jsonfile):
        try:
            with open(jsonfile, 'r') as file:
                data = json.load(file)
                return data
            print("JSON data loaded from file:")
            pprint.pprint(data)
        except FileNotFoundError:
            print("Error: 'data.json' not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in 'data.json'.")    
    #get_files_without_extensions
    def get_directory_files(directory, has_format=False):
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                # Remove the file extension
                if has_format:
                    files.append(item_path)
                else :
                    filename_without_ext = os.path.splitext(item)[0]
                    files.append(filename_without_ext)
        return files
    #main
    jsonfile = f'_outputs\\{str(project_num)}\\result.json'

    json_data = load_json( jsonfile )

    image_folder = os.path.join(json_data['path'], 'images')
    files_only = get_directory_files(image_folder, False)
    pprint.pprint(files_only)
    scene_dict = json_data['scenes']
    video_folder = f'_outputs\\{str(project_num)}\\videos'
    for key in files_only:
        scene = scene_dict[key]
        video_prompt = scene['scene']
        img_url = scene['image_url']

        # vid_path = generate_video( video_prompt, img_url, video_folder,  str(key)+'.mp4')
        
        # print(vid_path)

    video_files = get_directory_files(video_folder, True)
    
    joint = join_mp4_files( video_files, f"{video_folder}\\combined.mp4")
    

    
    #check existing images in folder

#get all ids

if __name__ == "__main__":
    main()