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

    scene_agent = SceneAgent( deepseek_client )
    scenes = scene_agent.generate("Adventurer at Macchu Pichu")
    pprint.pprint(scenes)

    project_num = 1
    folder = f'_outputs/{str(project_num)}'
    img_prompt_agent = ImagePromptAgent(deepseek_client)
    for i,scene in enumerate(scenes['scenes']):
        prompt = img_prompt_agent.generate(scene)['prompt']
        img_path = generate_image(prompt, folder, str(i)+'.jpg')
        print(img_path)
        
if __name__ == "__main__":
    main()