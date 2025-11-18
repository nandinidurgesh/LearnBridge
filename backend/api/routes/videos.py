"""
Video generation API routes
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import os

from ..models.schemas import (
    CreateVideoRequest,
    CreateVideoResponse,
    VideoStatusResponse,
    VideoHistoryResponse,
    DeleteVideoResponse,
    VideoStatus
)
from ..services.job_tracker import job_tracker
from ..services.video_service import start_video_generation


router = APIRouter(prefix="/api/videos", tags=["videos"])

# Storage directory
STORAGE_DIR = Path(__file__).parent.parent.parent / "storage"


@router.post("/generate", response_model=CreateVideoResponse)
async def generate_video(
    request: CreateVideoRequest,
    background_tasks: BackgroundTasks
):
    """
    Initiate video generation
    Returns job_id for status polling
    """
    # Create job
    job_id = job_tracker.create_job(request.topic, request.num_scenes)

    # Start generation in background
    background_tasks.add_task(
        start_video_generation,
        job_id,
        request.topic,
        request.num_scenes
    )

    return CreateVideoResponse(
        job_id=job_id,
        status=VideoStatus.PROCESSING
    )


@router.get("/status/{job_id}", response_model=VideoStatusResponse)
async def get_video_status(job_id: str):
    """
    Get status of video generation job
    Frontend polls this every 2 seconds
    """
    job = job_tracker.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return VideoStatusResponse(
        status=job.status,
        progress=job.progress,
        current_step=job.current_step,
        video_url=job.video_url,
        thumbnail_url=job.thumbnail_url,
        error_message=job.error_message
    )


@router.get("/history", response_model=VideoHistoryResponse)
async def get_video_history():
    """
    Get all videos (sorted by newest first)
    TODO: Implement "keep last 5" logic when requested
    """
    videos = job_tracker.get_all_jobs()

    # Filter only completed videos for history
    completed_videos = [v for v in videos if v.status == VideoStatus.COMPLETED]

    return VideoHistoryResponse(videos=completed_videos)


@router.get("/{video_id}/download")
async def download_video(video_id: str):
    """
    Download video file
    """
    video_path = STORAGE_DIR / "videos" / f"{video_id}.mp4"

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )


@router.delete("/{video_id}", response_model=DeleteVideoResponse)
async def delete_video(video_id: str):
    """
    Delete a video
    """
    # Delete from job tracker
    success = job_tracker.delete_job(video_id)

    if not success:
        raise HTTPException(status_code=404, detail="Video not found")

    # Delete files
    video_path = STORAGE_DIR / "videos" / f"{video_id}.mp4"
    thumbnail_path = STORAGE_DIR / "thumbnails" / f"{video_id}.jpg"

    if video_path.exists():
        os.remove(video_path)

    if thumbnail_path.exists():
        os.remove(thumbnail_path)

    return DeleteVideoResponse(success=True)
