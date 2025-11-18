import { useState, useEffect, useCallback } from 'react';
import { videoService } from '../services/videoService';
import type { CreateVideoRequest, VideoStatusResponse } from '../types/video.types';


export function useVideoGeneration() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<VideoStatusResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);


  const generateVideo = useCallback(async (data: CreateVideoRequest) => {
    try {
      setIsGenerating(true);
      setError(null);
      const response = await videoService.createVideo(data);
      setJobId(response.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start video generation');
      setIsGenerating(false);
    }
  }, []);

  useEffect(() => {
    if (!jobId || !isGenerating) return;

    const pollInterval = setInterval(async () => {
      try {
        const statusResponse = await videoService.getVideoStatus(jobId);
        setStatus(statusResponse);

        if (statusResponse.status === 'completed' || statusResponse.status === 'failed') {
          setIsGenerating(false);
          clearInterval(pollInterval);
        }

        if (statusResponse.status === 'failed') {
          setError(statusResponse.error_message || 'Video generation failed');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch status');
        setIsGenerating(false);
        clearInterval(pollInterval);
      }
    }, 2000); 

    return () => clearInterval(pollInterval);
  }, [jobId, isGenerating]);


  const reset = useCallback(() => {
    setJobId(null);
    setStatus(null);
    setIsGenerating(false);
    setError(null);
  }, []);

  return {
    generateVideo,
    reset,
    jobId,
    status,
    isGenerating,
    error,
    progress: status?.progress || 0,
    currentStep: status?.current_step,
    videoUrl: status?.video_url,
    thumbnailUrl: status?.thumbnail_url,
  };
}
