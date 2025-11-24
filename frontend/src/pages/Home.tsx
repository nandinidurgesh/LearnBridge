import { useState } from "react";
import { useVideoGeneration } from "../hooks/useVideoGeneration";
import { useVideoHistory } from "../hooks/useVideoHistory";
import { videoService } from "../services/videoService";
import Header from "../components/shared/Header";
import HistoryContainer from "../components/shared/HistoryContainer";
import VideoContainer from "../components/shared/VideoContainer";
import InputForm from "../components/shared/InputForm";

export default function Home() {
  const [topic, setTopic] = useState("");

  const {
    generateVideo,
    reset,
    isGenerating,
    error,
    progress,
    currentStep,
    videoUrl,
    thumbnailUrl,
  } = useVideoGeneration();

  const {
    videos,
    isLoading: historyLoading,
    deleteVideo,
    downloadVideo,
    fetchHistory,
  } = useVideoHistory();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    // num_scenes is now optional - backend auto-determines optimal count
    await generateVideo({ topic });
  };

  const handleCreateAnother = () => {
    reset();
    setTopic("");
    fetchHistory();
  };

  const handlePlayVideo = (_videoId: string, videoUrl: string) => {
    const fullUrl = videoService.getVideoUrl(videoUrl);
    window.open(fullUrl, "_blank");
  };

  const handleDownloadVideo = async (videoId: string, topic: string) => {
    try {
      await downloadVideo(videoId, `${topic}.mp4`);
    } catch (err) {
      console.error("Failed to download video:", err);
      alert("Failed to download video. Please try again.");
    }
  };

  const handleDeleteVideo = async (videoId: string) => {
    if (window.confirm("Are you sure you want to delete this video?")) {
      try {
        await deleteVideo(videoId);
      } catch (err) {
        console.error("Failed to delete video:", err);
        alert("Failed to delete video. Please try again.");
      }
    }
  };

  return (
    <div>
      <Header />
      <div className="flex flex-col items-center gap-4 md:flex-row md:items-start mt-4 h-[85vh] px-4">
        <div className="flex flex-col px-6 w-full md:w-4/5 h-auto md:h-full">
          <VideoContainer
            isGenerating={isGenerating}
            progress={progress}
            currentStep={currentStep}
            videoUrl={videoUrl}
            thumbnailUrl={thumbnailUrl}
            error={error}
            topic={topic}
          />

          {!videoUrl && (
            <InputForm
              topic={topic}
              onTopicChange={setTopic}
              onSubmit={handleSubmit}
              isLoading={isGenerating}
            />
          )}

          {videoUrl && !isGenerating && (
            <div className="mt-4">
              <button
                onClick={handleCreateAnother}
                className="w-full bg-white border-2 border-violet-500 text-violet-600 font-semibold py-3 px-6 rounded-xl hover:bg-violet-50 transition-all shadow-sm hover:shadow-md"
              >
                Create Another Video
              </button>
            </div>
          )}
        </div>

        <HistoryContainer
          videos={videos}
          isLoading={historyLoading}
          onPlayVideo={handlePlayVideo}
          onDownloadVideo={handleDownloadVideo}
          onDeleteVideo={handleDeleteVideo}
        />
      </div>
    </div>
  );
}
