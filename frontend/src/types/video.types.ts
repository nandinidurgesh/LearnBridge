export type VideoStatus = 'processing' | 'completed' | 'failed';

export type VideoStep = 'script' | 'images' | 'audio' | 'assembly';

export interface Video {
  id: string;
  topic: string;
  num_scenes?: number;
  status: VideoStatus;
  progress: number;
  current_step?: VideoStep;
  video_url?: string;
  thumbnail_url?: string;
  created_at: string;
  error_message?: string;
}

export interface CreateVideoRequest {
  topic: string;
  num_scenes?: number;
}

export interface CreateVideoResponse {
  job_id: string;
  status: VideoStatus;
}

export interface VideoStatusResponse {
  status: VideoStatus;
  progress: number;
  current_step?: VideoStep;
  video_url?: string;
  thumbnail_url?: string;
  error_message?: string;
}

export interface VideoHistoryResponse {
  videos: Video[];
}
