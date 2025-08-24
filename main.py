from dotenv import load_dotenv
from agents.scene_agent import SceneAgent
from agents.image_prompt_agent import ImagePromptAgent
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
    scenes = scene_agent.generate("Adventurer at Grand Canyon")
    pprint.pprint(scenes)

    img_prompt_agent = ImagePromptAgent(deepseek_client)
    for scene in scenes['scenes']:
        prompt = img_prompt_agent.generate(scene)['prompt']
        pprint.pprint(prompt)

    
if __name__ == "__main__":
    main()