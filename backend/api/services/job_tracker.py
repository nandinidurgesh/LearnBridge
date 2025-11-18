"""
In-memory job tracker for video generation
(Using dict instead of database for simplicity)
"""
from typing import Dict, Optional
from datetime import datetime
import uuid
from ..models.schemas import VideoStatus, VideoStep, Video


class JobTracker:
    """Tracks video generation jobs in memory"""

    def __init__(self):
        self.jobs: Dict[str, Video] = {}

    def create_job(self, topic: str, num_scenes: int) -> str:
        """Create a new job and return job_id"""
        job_id = str(uuid.uuid4())

        job = Video(
            id=job_id,
            topic=topic,
            num_scenes=num_scenes,
            status=VideoStatus.PROCESSING,
            progress=0,
            current_step=VideoStep.SCRIPT,
            created_at=datetime.now()
        )

        self.jobs[job_id] = job
        return job_id

    def get_job(self, job_id: str) -> Optional[Video]:
        """Get job by ID"""
        return self.jobs.get(job_id)

    def update_progress(
        self,
        job_id: str,
        progress: int,
        current_step: Optional[VideoStep] = None
    ):
        """Update job progress"""
        if job_id in self.jobs:
            self.jobs[job_id].progress = progress
            if current_step:
                self.jobs[job_id].current_step = current_step

    def mark_completed(
        self,
        job_id: str,
        video_url: str,
        thumbnail_url: Optional[str] = None
    ):
        """Mark job as completed"""
        if job_id in self.jobs:
            self.jobs[job_id].status = VideoStatus.COMPLETED
            self.jobs[job_id].progress = 100
            self.jobs[job_id].video_url = video_url
            self.jobs[job_id].thumbnail_url = thumbnail_url
            self.jobs[job_id].current_step = None

    def mark_failed(self, job_id: str, error_message: str):
        """Mark job as failed"""
        if job_id in self.jobs:
            self.jobs[job_id].status = VideoStatus.FAILED
            self.jobs[job_id].error_message = error_message
            self.jobs[job_id].current_step = None

    def get_all_jobs(self) -> list[Video]:
        """Get all jobs sorted by creation date (newest first)"""
        return sorted(
            self.jobs.values(),
            key=lambda x: x.created_at,
            reverse=True
        )

    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            return True
        return False


# Global job tracker instance
job_tracker = JobTracker()
