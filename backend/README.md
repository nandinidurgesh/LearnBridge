# Video Generation pipeline

1. Script Generator : uses google Gemini 2.0 Flash API for script generation.
   Earlier Mistral(Ollama) was being used as it is an offile model but it required a lot of disc space and the results were not as good hence the
   switch. The dependencies went down from 2GB+ to ~50MB.
   Analyses topic complexity(Obtained from frontend ) -> Decides how many scenes to produce based on complexity (10-20 scenes, auto-determined or user-specified up to 20 max) -> Outputs a JSON object with image prompt (scenes - to be consumed by image generation script) and narration text (to be consumed by audio generation script). Optimized for <10 seconds per scene. Each narration is 1-2 concise sentences (25-30 words max) focusing on core concepts.

2. Image Generation : Intitally stable diffusion as being used to geenrate images as it is a free resource but the images were more photographic than educational so first I migrated to using openai APIs(dalle-3) for image genration but it was expensive so switched to dalle-2 instead but still the cost was high and images were still leaning towards photographic than education relevant. So, decided to migrate to gemini to produce well labelled eucational svgs with text annotations and arrows, which are converted into pngs and stitched together to form explainatory videos. The cost went down from ~0.2$ per video to 0.03$ per video(for 5 scenes) and image quality improved drsatically in terms of relevance.

Rate Limiting: Implements smart rate limiting (9 calls/min) to handle Gemini API free tier limits (10 RPM). With 15-20 scenes, generation takes 2-4 minutes but ensures reliable API access.

Retry Logic : Includes exponential backoff retry logic (up to 3 attempts) for failed API calls to handle transient errors.

3. Audio Generation : uses google's text to speech for audio geenration from the JSON(narration_text) output created by script generator.

4. Video Assembler : Takes in audio and image files to create video. It takes in each image and shows it for the duration of it's audio. Uses zip() to pair image 1 with audio 1 and so on.

# Backend

Using fastAPI for API creation.
