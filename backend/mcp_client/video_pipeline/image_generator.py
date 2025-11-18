"""
Image generation using OpenAI DALL-E 2 or 3.
"""
import os
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

# Initialize OpenAI client
# API key will be read from environment variable OPENAI_API_KEY
client = OpenAI()


def generate_images(script, output_dir="output_images"):
    """
    Generate images using OpenAI DALL-E 3

    Args:
        script: Dictionary with 'scenes' list containing image_prompt for each scene
        output_dir: Directory to save generated images

    Returns:
        List of file paths to generated images
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for scene in script["scenes"]:
        prompt = scene["image_prompt"]
        scene_id = scene["id"]

        print(f"Generating image for Scene {scene_id}...")
        print(f"Prompt: {prompt}")

        try:
            # Generate image with DALL-E 3
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",  # DALL-E 3 supports: 1024x1024, 1792x1024, 1024x1792
                quality="standard",  # "standard" or "hd"
                n=1,
            )

            # Get the image URL from response
            image_url = response.data[0].url

            # Download the image
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            # Save the image
            file_path = os.path.join(output_dir, f"scene_{scene_id}.png")
            image.save(file_path)

            print(f"✓ Saved: {file_path}")
            results.append(file_path)

        except Exception as e:
            print(f"✗ Error generating image for Scene {scene_id}: {str(e)}")
            # Create a placeholder error image or raise exception
            raise Exception(f"Failed to generate image for scene {scene_id}: {str(e)}")

    return results


# Alternative: Use DALL-E 2 (faster, cheaper, but lower quality)
def generate_images_dalle2(script, output_dir="output_images"):
    """
    Generate images using OpenAI DALL-E 2 (cheaper alternative)
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for scene in script["scenes"]:
        prompt = scene["image_prompt"]
        scene_id = scene["id"]

        print(f"Generating image for Scene {scene_id} with DALL-E 2...")

        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="512x512",  # DALL-E 2 supports: 256x256, 512x512, 1024x1024
                n=1,
            )

            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            file_path = os.path.join(output_dir, f"scene_{scene_id}.png")
            image.save(file_path)

            print(f"✓ Saved: {file_path}")
            results.append(file_path)

        except Exception as e:
            print(f"✗ Error: {str(e)}")
            raise Exception(f"Failed to generate image for scene {scene_id}: {str(e)}")

    return results
