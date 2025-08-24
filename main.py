from dotenv import load_dotenv
from agents.scene_agent import SceneAgent
from agents.image_prompt_agent import ImagePromptAgent
from agents.image_agent import generate_image
load_dotenv()  # take environment variables
import os
from openai import OpenAI
import pprint
# python -m venv <myenv>
# .\myenv\Scripts\activate
def main():
    #openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    deepseek_client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

    #user inputs
    input_theme = "Tourist at Chile"
    project_num = 3

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
    results = []
    for i,scene in enumerate(scenes['scenes']):
        prompt = img_prompt_agent.generate(scene)['prompt']
        img_path = generate_image(prompt, output_img_folder, str(i)+'.jpg')

        result = {
            "id" : i,
            "scene" : scene,
            "image_prompt": prompt,
            "image_path" : img_path
        }

        results.append( result )
        
if __name__ == "__main__":
    main()