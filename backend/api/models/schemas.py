from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class VideoStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoStep(str, Enum):
    SCRIPT = "script"
    IMAGES = "images"
    AUDIO = "audio"
    ASSEMBLY = "assembly"


class CreateVideoRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200, description="Video topic")
    num_scenes: int = Field(..., ge=3, le=10, description="Number of scenes (3-10)")


class CreateVideoResponse(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    status: VideoStatus = Field(default=VideoStatus.PROCESSING)


class VideoStatusResponse(BaseModel):
    status: VideoStatus
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    current_step: Optional[VideoStep] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error_message: Optional[str] = None


class Video(BaseModel):
    id: str
    topic: str
    num_scenes: int
    status: VideoStatus
    progress: int
    current_step: Optional[VideoStep] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime
    error_message: Optional[str] = None


class VideoHistoryResponse(BaseModel):
    videos: List[Video]


class DeleteVideoResponse(BaseModel):
    success: bool
