

import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


def assemble_video(image_paths, audio_paths, output_path="final_video/output.mp4"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    clips = []

    for img_path, audio_path in zip(image_paths, audio_paths):
        print(f"Processing: {img_path}  +  {audio_path}")

        audio = AudioFileClip(audio_path)
        image = ImageClip(img_path).set_duration(audio.duration)

        image = image.set_audio(audio)

        clips.append(image)

    final = concatenate_videoclips(clips)
    final.write_videofile(output_path, fps=24)

    print(f"\n Video created: {output_path}")
    return output_path


# def main():
#     # small test
#     test_images = ["output_images/scene_1.png"]
#     test_audio = ["output_audio/scene_1.mp3"]

#     assemble_video(test_images, test_audio)


# if __name__ == "__main__":
#     main()
