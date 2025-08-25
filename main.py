from dotenv import load_dotenv
from agents.scene_agent import SceneAgent
from agents.image_prompt_agent import ImagePromptAgent
from agents.image_agent import generate_image
load_dotenv()  # take environment variables
import os
from openai import OpenAI
import pprint
import json
# python -m venv <myenv>
# .\myenv\Scripts\activate
def main():
    #openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    deepseek_client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

    #user inputs
    input_theme = "Tourist in Singapore. 1. Shopping at marina bay sands 2. Riding the singapore flyer overseeing the cityscape 3. Visting the art science museum 4. Catching the Formula 1 night show at Marina floating platform "
    project_num = 6

    #make folders
    folder = f'_outputs\\{str(project_num)}'
    output_img_folder = folder+'\\images'
    output_video_folder = folder+'\\videos'
    os.makedirs(folder, exist_ok=True)
    os.makedirs(output_img_folder, exist_ok=True)
    os.makedirs(output_video_folder, exist_ok=True)

    scene_agent = SceneAgent( deepseek_client )
    scenes = scene_agent.generate(input_theme)
    pprint.pprint(scenes)

    img_prompt_agent = ImagePromptAgent(deepseek_client)
    scene_outputs = {}
    for i,scene in enumerate(scenes['scenes']):
        prompt = img_prompt_agent.generate(scene)['prompt']
        img_url, img_path = generate_image(prompt, output_img_folder, str(i)+'.jpg')

        scene_output = {
            "scene" : scene,
            "image_prompt": prompt,
            "image_path" : img_path,
            "image_url" : img_url
        }

        scene_outputs[i] = scene_output
    
    result = {
        "theme" : input_theme,
        "path" : folder,
        "scenes" : scene_outputs
    }
    with open(folder + '\\result.json', 'w') as json_file:
        json.dump(result, json_file, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()