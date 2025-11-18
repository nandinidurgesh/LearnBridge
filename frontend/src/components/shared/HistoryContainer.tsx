import { Clock, Video, Play, Download, Trash2, Loader2 } from "lucide-react";
import type { Video as VideoType } from "../../types/video.types";
import { videoService } from "../../services/videoService";

interface HistoryContainerProps {
  videos: VideoType[];
  isLoading?: boolean;
  onPlayVideo?: (videoId: string, videoUrl: string) => void;
  onDownloadVideo?: (videoId: string, topic: string) => void;
  onDeleteVideo?: (videoId: string) => void;
}

export default function HistoryContainer({
  videos,
  isLoading = false,
  onPlayVideo,
  onDownloadVideo,
  onDeleteVideo,
}: HistoryContainerProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="w-80 space-y-4 mr-4">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Clock className="w-5 h-5 text-violet-600" />
          <h3 className="font-semibold text-slate-900">Recent Videos</h3>
        </div>

        {isLoading && (
          <div className="text-center py-8">
            <Loader2 className="w-8 h-8 text-violet-600 mx-auto mb-3 animate-spin" />
            <p className="text-sm text-slate-500">Loading history...</p>
          </div>
        )}

        {!isLoading && videos.length === 0 && (
          <div className="text-center py-8">
            <Clock className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <p className="text-sm text-slate-500">No videos yet</p>
          </div>
        )}

        {!isLoading && videos.length > 0 && (
          <div className="space-y-3 max-h-[600px] overflow-y-auto">
            {videos.map((video) => (
              <div
                key={video.id}
                className="group border border-slate-200 rounded-xl p-3 hover:border-violet-300 hover:shadow-sm transition-all"
              >
                {video.thumbnail_url && (
                  <div className="relative mb-2 rounded-lg overflow-hidden bg-slate-100">
                    <img
                      src={videoService.getThumbnailUrl(video.thumbnail_url)}
                      alt={video.topic}
                      className="w-full h-32 object-cover"
                    />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all flex items-center justify-center">
                      <Play className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-all" />
                    </div>
                  </div>
                )}

                <h4 className="font-semibold text-sm text-slate-900 mb-1 line-clamp-2">
                  {video.topic}
                </h4>

                <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
                  <div className="flex items-center gap-1">
                    <Video className="w-3 h-3" />
                    <span>{video.num_scenes} scenes</span>
                  </div>
                  <span>•</span>
                  <span>{formatDate(video.created_at)}</span>
                </div>

                {video.status !== "completed" && (
                  <div className="mb-2">
                    <span
                      className={`inline-block px-2 py-1 rounded-full text-xs font-semibold ${
                        video.status === "processing"
                          ? "bg-blue-100 text-blue-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {video.status}
                    </span>
                  </div>
                )}

                {video.status === "completed" && video.video_url && (
                  <div className="flex gap-1">
                    <button
                      onClick={() => onPlayVideo?.(video.id, video.video_url!)}
                      className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 bg-violet-50 text-violet-700 rounded-lg hover:bg-violet-100 transition-all text-xs font-medium"
                      title="Play video"
                    >
                      <Play className="w-3 h-3" />
                      Play
                    </button>
                    <button
                      onClick={() => onDownloadVideo?.(video.id, video.topic)}
                      className="flex items-center justify-center px-2 py-1.5 bg-slate-50 text-slate-700 rounded-lg hover:bg-slate-100 transition-all"
                      title="Download"
                    >
                      <Download className="w-3 h-3" />
                    </button>
                    <button
                      onClick={() => onDeleteVideo?.(video.id)}
                      className="flex items-center justify-center px-2 py-1.5 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-all"
                      title="Delete"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
