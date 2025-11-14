
import os
from gtts import gTTS

def generate_audio(script, output_dir="output_audio"):
    """
    Converts narration_text from script into MP3 files.
    """
    os.makedirs(output_dir, exist_ok=True)

    audio_paths = []

    for scene in script["scenes"]:
        scene_id = scene["id"]
        text = scene["narration_text"]

        print(f"Generating narration for Scene {scene_id}...")

        tts = gTTS(text)
        file_path = os.path.join(output_dir, f"scene_{scene_id}.mp3")
        tts.save(file_path)

        print(f"✔ Saved: {file_path}")

        audio_paths.append(file_path)

    return audio_paths


# def main():
#     # test
#     sample_script = {
#         "scenes": [
#             {"id": 1, "narration_text": "This is a test narration for scene one."}
#         ]
#     }
#     generate_audio(sample_script)


# if __name__ == "__main__":
#     main()
