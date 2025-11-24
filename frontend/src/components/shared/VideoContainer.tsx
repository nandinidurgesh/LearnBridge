import { Play, Video, Loader2, AlertCircle, CheckCircle } from "lucide-react";
import { videoService } from "../../services/videoService";

interface VideoContainerProps {
  isGenerating: boolean;
  progress: number;
  currentStep?: "script" | "images" | "audio" | "assembly";
  videoUrl?: string;
  thumbnailUrl?: string;
  error?: string | null;
  topic?: string;
}

export default function VideoContainer({
  isGenerating,
  progress,
  currentStep,
  videoUrl,
  error,
  topic,
}: VideoContainerProps) {
  const stepLabels = {
    script: "Generating Script",
    images: "Creating Images",
    audio: "Generating Audio",
    assembly: "Assembling Video",
  };

  const steps = ["script", "images", "audio", "assembly"] as const;

  if (error && !isGenerating) {
    return (
      <div className="w-full flex justify-center items-center h-3/5">
        <div className="bg-red-50 rounded-2xl border-2 border-red-200 p-12 text-center w-full h-full flex items-center justify-center flex-col">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-red-600" />
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Generation Failed
          </h3>
          <p className="text-slate-600 mb-4">{error}</p>
          <p className="text-sm text-slate-500">
            Please try again with a different topic
          </p>
        </div>
      </div>
    );
  }

  if (isGenerating) {
    return (
      <div className="w-full flex justify-center items-center h-3/5">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 w-full h-full flex items-center justify-center flex-col">
          <div className="mb-6">
            <Loader2 className="w-16 h-16 text-violet-600 animate-spin" />
          </div>

          <div className="w-full max-w-md mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-semibold text-slate-700">
                {currentStep ? stepLabels[currentStep] : "Starting..."}
              </span>
              <span className="text-sm font-bold text-violet-600">
                {progress}%
              </span>
            </div>
            <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-violet-500 to-purple-600 transition-all duration-500 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          <div className="flex items-center justify-center gap-4 mb-6">
            {steps.map((step, index) => {
              const isActive = currentStep === step;
              const isCompleted =
                steps.indexOf(currentStep || "script") > index;

              return (
                <div key={step} className="flex items-center">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                      isCompleted
                        ? "bg-green-500 text-white"
                        : isActive
                        ? "bg-violet-600 text-white ring-4 ring-violet-200"
                        : "bg-slate-200 text-slate-400"
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle className="w-5 h-5" />
                    ) : (
                      <span className="text-sm font-bold">{index + 1}</span>
                    )}
                  </div>
                  {index < steps.length - 1 && (
                    <div
                      className={`w-8 h-1 mx-2 ${
                        isCompleted ? "bg-green-500" : "bg-slate-200"
                      }`}
                    />
                  )}
                </div>
              );
            })}
          </div>

          <p className="text-slate-600 text-center">
            Creating your video about{" "}
            <span className="font-semibold text-violet-600">{topic}</span>
          </p>
          <p className="text-sm text-slate-500 mt-2">
            This usually takes 1-2 minutes...
          </p>
        </div>
      </div>
    );
  }

  if (videoUrl) {
    const fullVideoUrl = videoService.getVideoUrl(videoUrl);

    return (
      <div
        className="w-full flex justify-center items-center"
        style={{ height: "80vh" }}
      >
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden w-full h-full flex flex-col">
          <div className="relative flex-1 bg-black flex items-center justify-center">
            <video
              controls
              controlsList="nodownload"
              className="max-w-full max-h-full"
              src={fullVideoUrl}
              style={{
                width: "auto",
                height: "auto",
                maxHeight: "100%",
                maxWidth: "100%",
              }}
            >
              Your browser does not support video playback.
            </video>
          </div>

          <div className="p-6 border-t border-slate-200">
            <h3 className="text-xl font-bold text-slate-900 mb-4">
              {topic || "Your Video"}
            </h3>
            {/* <div className="flex gap-3">
              <a
                href={fullVideoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 bg-gradient-to-r from-violet-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-violet-600 hover:to-purple-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
              >
                <Play className="w-5 h-5" />
                Open in New Tab
              </a>
              <a
                href={fullVideoUrl}
                download
                className="px-6 py-3 border-2 border-slate-300 text-slate-700 font-semibold rounded-xl hover:bg-slate-50 transition-all"
              >
                Download
              </a>
            </div> */}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full flex justify-center items-center h-3/5">
      <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-2xl border-2 border-dashed border-violet-200 p-12 text-center w-full h-full flex items-center justify-center flex-col">
        <div className="w-16 h-16 bg-violet-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Video className="w-8 h-8 text-violet-600" />
        </div>
        <h3 className="text-lg font-semibold text-slate-900 mb-2">
          Ready to Create
        </h3>
        <p className="text-slate-600">
          Enter a topic and number of scenes below to generate your first
          explainer video
        </p>
      </div>
    </div>
  );
}
