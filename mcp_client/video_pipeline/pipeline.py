from script_generator import generate_script
from image_generator import generate_images
from audio_generator import generate_audio
from video_assembler import assemble_video


def create_video(topic: str, num_scenes: int = 4):
    print("\n=== Generating Script ===")
    script = generate_script(topic, num_scenes)

    print("\n=== Generating Images ===")
    image_paths = generate_images(script)

    print("\n=== Generating Audio ===")
    audio_paths = generate_audio(script)

    print("\n=== Assembling Final Video ===")
    final_path = assemble_video(image_paths, audio_paths)

    print("\n🎉 COMPLETED! Final video saved at:", final_path)


def main():
    topic = input("Enter topic: ")
    scenes = int(input("Number of scenes: "))

    create_video(topic, scenes)


if __name__ == "__main__":
    main()
