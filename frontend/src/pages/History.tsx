import { useVideoHistory } from "../hooks/useVideoHistory";
import { videoService } from "../services/videoService";
import { Play, Download, Trash2, Video, Loader2 } from "lucide-react";

export default function History() {
  const { videos, isLoading, error, deleteVideo, downloadVideo } =
    useVideoHistory();

  const handleDelete = async (videoId: string) => {
    if (window.confirm("Are you sure you want to delete this video?")) {
      try {
        await deleteVideo(videoId);
      } catch (err) {
        alert(err instanceof Error ? err.message : "Failed to delete video");
      }
    }
  };

  const handleDownload = async (videoId: string, topic: string) => {
    try {
      await downloadVideo(videoId, `${topic}.mp4`);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to download video");
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            Your Videos
          </h1>
          <p className="text-slate-600 mb-8">Last 5 generated videos</p>
          <div className="flex justify-center items-center py-20">
            <Loader2 className="w-12 h-12 text-violet-600 animate-spin" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">
            Your Videos
          </h1>
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <p className="text-red-700">Error: {error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Your Videos</h1>
        <p className="text-slate-600 mb-8">Last 5 generated videos</p>

        {videos.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center">
            <Video className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-lg font-semibold text-slate-900 mb-2">
              No videos yet
            </p>
            <p className="text-slate-600">
              Create your first educational video!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {videos.map((video) => (
              <div
                key={video.id}
                className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow relative"
              >
                {video.thumbnail_url && (
                  <div className="relative">
                    <img
                      src={videoService.getThumbnailUrl(video.thumbnail_url)}
                      alt={video.topic}
                      className="w-full h-48 object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                  </div>
                )}

                <div className="p-6">
                  <h3 className="text-lg font-bold text-slate-900 mb-2 line-clamp-2">
                    {video.topic}
                  </h3>

                  <div className="flex items-center gap-4 text-sm text-slate-600 mb-4">
                    <div className="flex items-center gap-1">
                      <Video className="w-4 h-4" />
                      <span>{video.num_scenes} scenes</span>
                    </div>
                    <span>•</span>
                    <span>
                      {new Date(video.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  {video.video_url && (
                    <div className="flex gap-2">
                      <button
                        onClick={() =>
                          window.open(
                            videoService.getVideoUrl(video.video_url!),
                            "_blank"
                          )
                        }
                        className="flex-1 flex items-center justify-center gap-2 bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-violet-700 transition-all"
                        title="Play video"
                      >
                        <Play className="w-4 h-4" />
                        Play
                      </button>
                      <button
                        onClick={() => handleDownload(video.id, video.topic)}
                        className="flex items-center justify-center px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-all"
                        title="Download"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(video.id)}
                        className="flex items-center justify-center px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-all"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  )}

                  {video.status !== "completed" && (
                    <div className="absolute top-4 right-4">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          video.status === "processing"
                            ? "bg-blue-100 text-blue-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {video.status}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
