import type { FormEvent } from 'react';

interface InputFormProps {
  topic: string;
  numScenes: number;
  onTopicChange: (value: string) => void;
  onScenesChange: (value: number) => void;
  onSubmit: (e: FormEvent) => void;
  isLoading?: boolean;
}

export default function InputForm({
  topic,
  numScenes,
  onTopicChange,
  onScenesChange,
  onSubmit,
  isLoading = false,
}: InputFormProps) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 mt-4">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">
          Create Your Explainer Video
        </h2>
        <p className="text-slate-600">
          Enter a topic and number of scenes to generate an educational video
        </p>
      </div>

      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Topic
          </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => onTopicChange(e.target.value)}
            placeholder="e.g., The Water Cycle, Pythagorean Theorem, French Revolution..."
            className="w-full px-4 py-2 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent text-slate-900 placeholder:text-slate-400 disabled:bg-slate-100 disabled:cursor-not-allowed"
            disabled={isLoading}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Number of Scenes
          </label>
          <input
            type="number"
            value={numScenes}
            onChange={(e) => onScenesChange(Number(e.target.value))}
            placeholder="3-10 scenes recommended"
            min="3"
            max="10"
            className="w-full px-4 py-2 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent text-slate-900 placeholder:text-slate-400 disabled:bg-slate-100 disabled:cursor-not-allowed"
            disabled={isLoading}
            required
          />
          <p className="mt-2 text-sm text-slate-500">
            Each scene is approximately 20-30 seconds
          </p>
        </div>

        <button
          type="submit"
          disabled={isLoading || !topic.trim()}
          className="w-full bg-gradient-to-r from-violet-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-violet-600 hover:to-purple-700 transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:from-violet-500 disabled:hover:to-purple-600"
        >
          {isLoading ? 'Generating...' : 'Generate Video'}
        </button>
      </form>
    </div>
  );
}
