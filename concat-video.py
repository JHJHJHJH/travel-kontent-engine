
import json
import pprint
import os
from agents.video_agent import join_mp4_files

if __name__ == "__main__":
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
    
    project_num = 8
    video_waudio_folder = f'_outputs\\{str(project_num)}\\videos_waudio'
    video_files = get_directory_files(video_waudio_folder, True)
    joint = join_mp4_files( video_files, f"_outputs\\{str(project_num)}\\final.mp4")