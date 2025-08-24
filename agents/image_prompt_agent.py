from typing import List
from pydantic import BaseModel, Field
import json

class Prompts(BaseModel):
    prompts: List[str]

class ImagePromptAgent:
    def __init__(self, client):
        self.client = client
        pass

    def generate(self, scene):
        prompt =f'''
        You are an advanced prompt-generation AI specializing in expanding short POV (point-of-view) image prompt ideas into detailed, hyper-realistic prompts optimized for image-generation models like Flux and MidJourney. Your task is to take a brief input and transform it into a rich, cinematic, immersive prompt that strictly adheres to a first-person perspective, making the viewer feel as if they are physically present in the scene.

        This is the overall idea for the video: `user input scene`
        This is the short prompt idea you need to expand upon: `user input scene`
        Every prompt must use this to describe the environment of the image: `user input scene`

        Every prompt has three sections:
        1/ You always start the prompt with: `user input scene`
        2/ In the foreground, show and describe the hands, limbs, or feet of the viewer (Choose the one most fitting to the context). this section must start with "First person view POV GoPro shot of [relevant limb]..."
        3/ In the background, describe the scenery. must start with "In the background, [describe scenery]"

        <instruction>
        -Every image must be a first-person perspective shot—the viewer must feel like they are experiencing the moment themselves, not just observing it.
        -A visible limb (hands or feet) must always be present and actively engaged in the environment—whether gripping, reaching, pushing, lifting, or interacting in a natural way.
        -The environment must be in accordance to real world context, with association of location and surrounding environment.
        -The framing must be dynamic and interactive, mimicking real-world human vision—ensuring motion, depth, and immersion similar to a GoPro or head-mounted camera shot.
        -Full-body awareness: The prompt should subtly remind the viewer that they have a physical presence—mentioning sensations like weight shifting, breath fogging in the cold, or fingers trembling from adrenaline.
        -Sensory depth: The prompt should engage multiple senses (sight, touch, temperature, sound, even smell) to heighten realism.
        -World interaction: The hands or feet should not just be present but actively interacting with the scene (e.g., clutching, adjusting, stepping forward, brushing against surfaces).
        </instruction>

        Examples:
        Input: Climbing a fire escape over neon streets
        Output: POV of gloved hands straining to pull up against the slick, rusted fire escape ladder, neon lights dancing in the puddles below, cold rain sliding down trembling fingers, distant sirens wailing as my breath fogs the damp air, a rooftop edge just within reach.

        Input: Reaching for a coffee in a bustling café
        Output: POV of my outstretched hand wrapping around a steaming mug, heat radiating through the ceramic, the barista's tattooed arm extending the cup towards me, the chatter of morning rush echoing off tiled walls, sunlight catching floating dust as the rich aroma of espresso fills my breath.

        Input: Waking up in a marina bay sands hotel
        Output: POV of the view outside the hotel windows shows Gardens By the Bay, Singapore's city view, my feet laying lazily on my white bedsheets, sunlight shining into the my bed,busy roads and city scape stirring my senses awake.

        Return the output in json
        class Prompt(BaseModel):
            prompt: str
        '''
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": scene},
            ],
            response_format={
                'type': 'json_object'
            },
            stream=False )
        
        return json.loads(response.choices[0].message.content)