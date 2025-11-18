
import json
from langchain_ollama import ChatOllama


MODEL = "mistral"

SYSTEM_PROMPT = """
You generate structured educational video scripts.

Output a JSON dictionary with this structure:

{
  "title": "...",
  "scenes": [
    {
      "id": 1,
      "image_prompt": "...",
      "narration_text": "..."
    }
  ]
}

Rules:
- Keep scenes simple and visually describable.
- `image_prompt` must describe a single clear image.
- `narration_text` must be one paragraph of simple student-friendly explanation.
- NO extra commentary. Output ONLY the JSON.
"""

def generate_script(topic: str, num_scenes: int = 4):
    llm = ChatOllama(model=MODEL, temperature=0.4)

    user_prompt = f"""
    Create an educational video script about: {topic}
    Number of scenes: {num_scenes}
    """

    response = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = response.content.strip()

    try:
        script = json.loads(response.content)
    except:
        raise ValueError("Model did not return valid JSON:\n" + response.content)

    for scene in script.get("scenes", []):
        if "narration_text" not in scene or not scene["narration_text"]:
            scene["narration_text"] = "This scene explains the concept shown in the diagram in a simple manner suitable for students."

    return script


# def main():
#     topic = "Water Cycle"
#     script = generate_script(topic, num_scenes=4)
#     print(json.dumps(script, indent=2))


# if __name__ == "__main__":
#     main()
