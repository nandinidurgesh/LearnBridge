"""
Video generation service that wraps the existing video pipeline
"""
import os
import sys
import asyncio
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import shutil

# Add mcp_client to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from mcp_client.video_pipeline.script_generator import generate_script
from mcp_client.video_pipeline.image_generator import generate_images_dalle2
from mcp_client.video_pipeline.audio_generator import generate_audio
from mcp_client.video_pipeline.video_assembler import assemble_video
from .job_tracker import job_tracker
from ..models.schemas import VideoStep


# Thread pool for running video generation in background
executor = ThreadPoolExecutor(max_workers=2)


def generate_video_sync(job_id: str, topic: str, num_scenes: int):
    """
    Synchronous video generation function (runs in thread pool)
    This wraps your existing video pipeline with progress tracking
    """
    try:
        # Create job-specific directories
        storage_dir = backend_dir / "storage"
        job_dir = storage_dir / "temp" / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        images_dir = job_dir / "images"
        audio_dir = job_dir / "audio"
        images_dir.mkdir(exist_ok=True)
        audio_dir.mkdir(exist_ok=True)

        # Step 1: Generate Script (0-25%)
        print(f"[Job {job_id}] Generating script for: {topic}")
        job_tracker.update_progress(job_id, 5, VideoStep.SCRIPT)

        script = generate_script(topic, num_scenes)
        job_tracker.update_progress(job_id, 25, VideoStep.SCRIPT)

        # Step 2: Generate Images (25-60%)
        print(f"[Job {job_id}] Generating images...")
        job_tracker.update_progress(job_id, 30, VideoStep.IMAGES)

        image_paths = generate_images_dalle2(script, str(images_dir))
        job_tracker.update_progress(job_id, 60, VideoStep.IMAGES)

        # Step 3: Generate Audio (60-80%)
        print(f"[Job {job_id}] Generating audio...")
        job_tracker.update_progress(job_id, 65, VideoStep.AUDIO)

        audio_paths = generate_audio(script, str(audio_dir))
        job_tracker.update_progress(job_id, 80, VideoStep.AUDIO)

        # Step 4: Assemble Video (80-100%)
        print(f"[Job {job_id}] Assembling video...")
        job_tracker.update_progress(job_id, 85, VideoStep.ASSEMBLY)

        # Save final video to storage/videos
        videos_dir = storage_dir / "videos"
        videos_dir.mkdir(exist_ok=True)
        output_path = videos_dir / f"{job_id}.mp4"

        assemble_video(image_paths, audio_paths, str(output_path))
        job_tracker.update_progress(job_id, 95, VideoStep.ASSEMBLY)

        # Generate thumbnail (first frame)
        thumbnail_path = storage_dir / "thumbnails" / f"{job_id}.jpg"
        thumbnail_path.parent.mkdir(exist_ok=True)
        generate_thumbnail(str(image_paths[0]), str(thumbnail_path))

        # Mark as completed
        video_url = f"/storage/videos/{job_id}.mp4"
        thumbnail_url = f"/storage/thumbnails/{job_id}.jpg"
        job_tracker.mark_completed(job_id, video_url, thumbnail_url)

        print(f"[Job {job_id}] Completed successfully!")

        # Cleanup temp directory
        shutil.rmtree(job_dir, ignore_errors=True)

    except Exception as e:
        print(f"[Job {job_id}] Failed with error: {str(e)}")
        job_tracker.mark_failed(job_id, str(e))


def generate_thumbnail(image_path: str, thumbnail_path: str):
    """Generate thumbnail from first image"""
    try:
        from PIL import Image

        img = Image.open(image_path)
        # Resize to thumbnail size
        img.thumbnail((320, 240))
        img.save(thumbnail_path, "JPEG", quality=85)
    except Exception as e:
        print(f"Failed to generate thumbnail: {e}")
        # If thumbnail generation fails, just copy the original image
        shutil.copy(image_path, thumbnail_path)


async def start_video_generation(job_id: str, topic: str, num_scenes: int):
    """
    Start video generation in background thread
    (Async wrapper for the sync function)
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        executor,
        generate_video_sync,
        job_id,
        topic,
        num_scenes
    )
