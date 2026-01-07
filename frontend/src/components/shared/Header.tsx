import { Video, Sparkles } from "lucide-react";

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200">
      <div className="max-w-full mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl flex items-center justify-center">
            <Video className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">LearnBridge</h1>
            <p className="text-xs text-slate-500">
              AI-Powered Awareness Videos{" "}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-violet-50 rounded-lg">
          <Sparkles className="w-4 h-4 text-violet-600" />
          <span className="text-sm font-medium text-violet-700">
            Free Credits: Unlimited{" "}
          </span>
        </div>
      </div>
    </header>
  );
}
