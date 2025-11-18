# LearnBridge Backend

Backend :
cd backend
pip install -r requirements.txt
install Python 3.11.x not 3.12+ as MoviePy has compatibility issues.
ollama serve : check at http://localhost:11434

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
or
python -m api.main
check at: http://localhost:8000

Frontend:

npm i
npm run dev

How It Works

1. Video Generation Request
   Frontend sends POST to /api/videos/generate
   Backend creates job ID and starts generation in background thread
   Returns job ID immediately

2. Background Processing
   Runs video pipeline:
   Script generation (Mistral LLM)
   Image generation (Stable Diffusion)
   Audio generation (gTTS)
   Video assembly (MoviePy)
   Updates progress in job tracker

3. Status Polling
   Frontend polls /api/videos/status/{job_id} every 2 seconds
   Backend returns current progress, step, and status
   When complete, returns video_url

4. Video Serving
   Videos served as static files from /storage/videos/
   Frontend displays video in <video> element

Deployment recommendations:
Backend: Railway, Render, or Fly.io (needs long-running process support)
Frontend: Vercel or Netlify
Why separate: Vercel serverless functions have 60s timeout, video generation takes 1-2 minutes
