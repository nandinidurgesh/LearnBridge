
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash-exp"

SYSTEM_PROMPT = """You are an expert educational content creator specializing in creating structured video scripts for learning materials.

                Your task is to generate educational video scripts in JSON format.

                Output ONLY a valid JSON object with this EXACT structure (no markdown, no code blocks, no extra text):

                {
                "title": "Clear, descriptive title",    
                "scenes": [
                    {
                    "id": 1,
                    "image_prompt": "Detailed prompt for educational diagram",
                    "narration_text": "Clear, student-friendly explanation"
                    }
                ]
                }

                CRITICAL RULES for determining number of scenes:
                - Analyze the topic complexity and determine optimal scene count (10-20 scenes)
                - Simple topics (e.g., "Basic shapes"): 10-12 scenes
                - Moderate topics (e.g., "Water cycle", "Cell division"): 12-16 scenes
                - Complex topics (e.g., "Photosynthesis", "Quantum mechanics"): 16-20 scenes
                - Each scene should cover ONE focused concept or step
                - Break down complex processes into clear, sequential steps with MORE granularity
                - More scenes = shorter, punchier explanations per scene

                CRITICAL RULES for image_prompt:
                - Each prompt will be used to generate an SVG educational diagram
                - Focus on LABELED DIAGRAMS with clear text annotations
                - Use "textbook illustration style" or "educational infographic"
                - Include "labeled diagram showing..." or "annotated diagram of..."
                - Request arrows, labels, and process flow indicators
                - Emphasize HIGH CONTRAST colors on white background
                - Use simple geometric shapes (circles, rectangles, arrows)
                - NO photorealistic requests, NO artistic interpretation
                - Be SPECIFIC about what labels and annotations should appear
                - Examples: "Labeled diagram showing the water cycle with arrows indicating evaporation, condensation, precipitation, and collection. Include clear text labels for each stage."

                CRITICAL RULES for narration_text (VERY IMPORTANT):
                - Write EXACTLY 1-2 concise sentences with a MAXIMUM of 25-30 words total
                - Focus on the single most important concept for this scene
                - Be clear and direct - no unnecessary elaboration
                - Target 8-10 seconds of audio duration when spoken naturally
                - Each narration should be a focused, memorable statement
                - Use simple, active voice and avoid complex sentence structures
                - Match the diagram content but keep explanation brief and punchy

                Examples of GOOD narration (concise, 8-10 seconds):
                - "Photosynthesis converts sunlight into chemical energy in plant cells. Chloroplasts contain chlorophyll which captures light to produce glucose and oxygen."
                - "The water cycle moves water through Earth's systems. Heat from the sun causes water to evaporate into the atmosphere."

                Examples of BAD narration (too long, over 10 seconds):
                - "Photosynthesis is the process by which plants convert sunlight into chemical energy stored in glucose. This happens in specialized structures called chloroplasts, which contain the green pigment chlorophyll that absorbs light energy."

                Output ONLY the JSON. No markdown formatting, no code blocks, no explanatory text."""

def generate_script(topic: str, num_scenes: int = None):
    try:
        model = genai.GenerativeModel(
            model_name = MODEL,
            generation_config={
                "temperature": 0.4, 
                "top_p": 0.95,
                "top_k": 40, 
                "max_output_tokens": 8192,
            }
        )
        if num_scenes:
            user_prompt = f"""Create an educational video script about: {topic}
                Number of scenes: {num_scenes}
                Remember:
                - Each image_prompt must request a LABELED EDUCATIONAL DIAGRAM with SPECIFIC labels mentioned
                - Use phrases like "labeled diagram", "educational infographic", "annotated illustration"
                - Request clear text labels, arrows, and high contrast colors
                - Focus on textbook-style diagrams, not photographs or artistic renders
                - Write CONCISE narration (1-2 sentences, 25-30 words MAX) that focuses on the core concept
                - Target 8-10 seconds of audio per scene

                Generate the JSON script now."""
        else:
            user_prompt = f"""Create an educational video script about: {topic}

                IMPORTANT: Determine the optimal number of scenes (10-20) based on topic complexity:
                - Simple topics: 10-12 scenes
                - Moderate complexity: 12-16 scenes
                - Complex topics: 16-20 scenes

                Remember:
                - Each image_prompt must request a LABELED EDUCATIONAL DIAGRAM with SPECIFIC labels mentioned
                - Use phrases like "labeled diagram", "educational infographic", "annotated illustration"
                - Request clear text labels, arrows, and high contrast colors
                - Focus on textbook-style diagrams, not photographs or artistic renders
                - Write CONCISE narration (1-2 sentences, 25-30 words MAX) that focuses on the core concept
                - Target 8-10 seconds of audio per scene
                - Each scene should cover ONE focused concept

                Generate the JSON script now."""

        chat = model.start_chat(history=[])

        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"
        response = chat.send_message(full_prompt)

        content = response.text.strip()

        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            script = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Gemini did not return valid JSON: {str(e)}\n\nResponse:\n{content}")

        if "scenes" not in script:
            raise ValueError("Script missing 'scenes' field")

        if not isinstance(script["scenes"], list):
            raise ValueError("'scenes' must be a list")

        for scene in script["scenes"]:
            if "id" not in scene:
                raise ValueError(f"Scene missing 'id' field: {scene}")
            if "image_prompt" not in scene or not scene["image_prompt"]:
                raise ValueError(f"Scene {scene.get('id')} missing 'image_prompt'")
            if "narration_text" not in scene or not scene["narration_text"]:
                scene["narration_text"] = "This scene explains the concept shown in the diagram."

        print(f"Generated script with {len(script['scenes'])} scenes")
        return script

    except Exception as e:
        raise Exception(f"Failed to generate script with Gemini: {str(e)}")
