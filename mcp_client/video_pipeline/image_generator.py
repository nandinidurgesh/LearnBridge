# mcp_client/video_pipeline/image_generator.py

import os
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

MODEL_ID = "stabilityai/sd-turbo"   


def load_pipeline():
    """
    Loads Stable Diffusion with MPS (Apple Silicon) acceleration.
    """
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16
    ).to("mps")

    return pipe


def generate_images(script, output_dir="output_images"):
    """
    Takes the JSON script from the LLM and generates all scene images.
    """
    os.makedirs(output_dir, exist_ok=True)

    pipe = load_pipeline()

    results = []

    for scene in script["scenes"]:
        prompt = scene["image_prompt"]
        scene_id = scene["id"]

        print(f"Generating image for Scene {scene_id}...")

        image = pipe(
            prompt,
            num_inference_steps=4
        ).images[0]

        file_path = os.path.join(output_dir, f"scene_{scene_id}.png")
        image.save(file_path)

        print(f"✔ Saved: {file_path}")
        results.append(file_path)

    return results


# def main():
#     script = {
#         "scenes": [
#             {"id": 1, "image_prompt": "A simple cartoon sun shining over water"}
#         ]
#     }
#     generate_images(script)


# if __name__ == "__main__":
#     main()
