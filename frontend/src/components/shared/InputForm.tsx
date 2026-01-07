import type { FormEvent } from "react";

interface InputFormProps {
  topic: string;
  onTopicChange: (value: string) => void;
  onSubmit: (e: FormEvent) => void;
  isLoading?: boolean;
}

export default function InputForm({
  topic,
  onTopicChange,
  onSubmit,
  isLoading = false,
}: InputFormProps) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 mt-4">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">
          Create Your Awareness Video
        </h2>
        <p className="text-slate-600">
          Enter any social awareness topic and we'll automatically create an
          informative video with diagrams, statistics, and narration
        </p>
      </div>

      <form onSubmit={onSubmit} className="space-y-3">
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Topic
          </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => onTopicChange(e.target.value)}
            placeholder="e.g., Effects of prolonged alcohol consumption on human body"
            className="w-full px-4 py-2 text-lg border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent text-slate-900 placeholder:text-slate-400 disabled:bg-slate-100 disabled:cursor-not-allowed"
            disabled={isLoading}
            required
          />
          <p className="mt-2 text-sm text-slate-500">
            We'll automatically determine the optimal length and number of
            scenes based on your topic's complexity
          </p>
        </div>

        <button
          type="submit"
          disabled={isLoading || !topic.trim()}
          className="w-full bg-gradient-to-r from-violet-500 to-purple-600 text-white font-semibold py-2 px-6 rounded-xl hover:from-violet-600 hover:to-purple-700 transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-violet-500 disabled:hover:to-purple-600 text-lg"
        >
          {isLoading ? "Generating Your Video..." : "Generate Video"}
        </button>
      </form>
    </div>
  );
}
