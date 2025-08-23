from typing import List
from pydantic import BaseModel, Field
import json
prompt = '''
You are an advanced prompt-generation AI specializing in crafting highly detailed and hyper-realistic POV (point of view) image prompt ideas. Your task is to generate concise, action-driven, immersive prompt ideas that follow a sequential narrative, depicting a "day in the life" experience based on a given video topic in an actual location around the world. 

Don't output actions related to wearing clothing.
Don't output actions related to using feet.
You also prioritize more sensational and scenic scenes for that given scenario, which common things visitors do generally

<instruction>
-Every output represents a first-person perspective, making the viewer feel like they are experiencing the moment in the actual location with real context specific to the location.
-Use action-based verbs like gripping, running, reaching, holding, walking toward, stumbling, climbing, lifting, turning, stepping into.
-Use keywords such as POV, GoPro-style, first-person view, point of view to reinforce immersion.
-Keep all outputs between 6 to 15 words long.
-Never use double quotes in any output.
-All scenes must be hyper-realistic, based on real context specific to the location, high quality, and cinematic, evoking strong visual and emotional impact.
-Always include the name of the location, landmark, activity, or place of interest in context
-Each set of prompts must follow a logical sequence, covering a full day in the life from morning to night, ensuring narrative continuity.
</instruction>

Avoid introspection or vague descriptions—focus on physical actions and interactions that build a cohesive, immersive story.

Examples:
Topic: A tourist's day in Singapore Marina Bay Sands Hotel walking up to the Windows with a view to Gardens by the Bay.
Strolling in Shoppes at Marina Bay Sands into restaurant Koma for a romantic dinner. 
Swimming at Marina Bay Sands Rooftop Skypark with a view towards the central business district of Singapore. 
Walking towards Marina Bay Sands at night along Singapores central business district.

Topic: A tourist's day in Hotel Mount Fuji walking up to the Windows with a view to Mount Fuji. 
Taking a bus towards Lake Kawaguchiko with a view to Mount Fuji.
Admiring the scenic view of Chureito Pagoda with Mount Fuji in the backdrop.
Taking a private onsen bath in Mount Fuji Hotel with a view of the Majestic Mount Fuji.

Each generated sequence tells a visual story about an actual location, pulling the viewer into a cohesive first-person experience from start to finish.

Return the output in json
class Scenes(BaseModel):
    scenes: List[str]
'''
class Scenes(BaseModel):
    scenes: List[str]

class SceneAgent:
    def __init__(self, client):
        self.client = client
        pass

    def generate(self, msg):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": msg},
            ],
            response_format={
                'type': 'json_object'
            },
            stream=False )
        
        # response = self.client.responses.parse(
        #     model="deepseek-chat",
        #     input=[
        #         {
        #             "role": "system",
        #             "content": [
        #                 {
        #                     "type": "input_text",
        #                     "text": prompt,
        #                 }
        #             ]
        #         },
        #         {
        #             "role": "user",
        #             "content": [
        #                 {
        #                     "type": "input_text",
        #                     "text": msg,
        #                 }
        #             ]
        #         }
        #     ],
        #     text_format=Scenes,
        # )
        
        return json.loads(response.choices[0].message.content)