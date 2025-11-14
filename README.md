It is an intelligent educational assistant that answers questions using Wikipedia and generates interactive videos with narration.
Uses Mistral(Offline support) LLM via Ollama for intelligent responses and google text to speech for narration. The video is geenrated using:

1. Mistral - generated script
2. Stable Diffusion (HuggingFace Diffusers + PyTorch MPS) - image generation based on scenes (json) produced by Mistral
3. GTTS - audio geenration
4. MoviePy - assembled images and audio to create video.

Installation :

1. Install python3, ollama and pull mistral.
2. create virtual environment : python3 -m venv venv, source venv/bin/activate(mac)
3. Install requirements: pip install -r requirements.txt
4. python3 mcp_client/pipeline.py

Other considerations:

1. Use Python 3.11.x - 3.12+ breaks MoviePy and some diffusers builds.
2. Using Apple-Silicon optimized PyTorch
3. generates simple explanatory videos, not photorealistic animation.

Future Improvements :

1. Multilingual support
