import { apiClient } from './api';
import type {
  CreateVideoRequest,
  CreateVideoResponse,
  VideoStatusResponse, 
  VideoHistoryResponse,
} from '../types/video.types';

export const videoService = {

  async createVideo(data: CreateVideoRequest): Promise<CreateVideoResponse> {
    const response = await apiClient.post<CreateVideoResponse>('/api/videos/generate', data);
    return response.data;
  },

  async getVideoStatus(jobId: string): Promise<VideoStatusResponse> {
    const response = await apiClient.get<VideoStatusResponse>(`/api/videos/status/${jobId}`);
    return response.data;
  },


  async getVideoHistory(): Promise<VideoHistoryResponse> {
    const response = await apiClient.get<VideoHistoryResponse>('/api/videos/history');
    return response.data;
  },


  async downloadVideo(videoId: string): Promise<Blob> {
    const response = await apiClient.get(`/api/videos/${videoId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },

 
  async deleteVideo(videoId: string): Promise<{ success: boolean }> {
    const response = await apiClient.delete(`/api/videos/${videoId}`);
    return response.data;
  },


  getVideoUrl(videoUrl: string): string {
    if (videoUrl.startsWith('http')) {
      return videoUrl;
    }
    return `${apiClient.defaults.baseURL}${videoUrl}`;
  },

  getThumbnailUrl(thumbnailUrl: string): string {
    if (thumbnailUrl.startsWith('http')) {
      return thumbnailUrl;
    }
    return `${apiClient.defaults.baseURL}${thumbnailUrl}`;
  },
};
