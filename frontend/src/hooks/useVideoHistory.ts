import { useState, useEffect, useCallback } from 'react';
import { videoService } from '../services/videoService';
import type { Video } from '../types/video.types';


export function useVideoHistory() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);


  const fetchHistory = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await videoService.getVideoHistory();
      setVideos(response.videos);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch video history');
    } finally {
      setIsLoading(false);
    }
  }, []);

 
  const deleteVideo = useCallback(async (videoId: string) => {
    try {
      await videoService.deleteVideo(videoId);
      setVideos((prev) => prev.filter((v) => v.id !== videoId));
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Failed to delete video');
    }
  }, []);

  const downloadVideo = useCallback(async (videoId: string, filename: string) => {
    try {
      const blob = await videoService.downloadVideo(videoId);
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || `video-${videoId}.mp4`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Failed to download video');
    }
  }, []);

  
  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    videos,
    isLoading,
    error,
    fetchHistory,
    deleteVideo,
    downloadVideo,
  };
}
