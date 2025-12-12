
import os
import re
import time
from datetime import datetime, timedelta
import google.generativeai as genai
import cairosvg
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class RateLimiter:
    """Rate limiter to handle Gemini API rate limits (10 requests per minute for free tier)"""

    def __init__(self, calls_per_minute=9):
        """
        Initialize rate limiter.

        Args:
            calls_per_minute: Maximum API calls allowed per minute.
                            Default is 9 (slightly below the 10/min limit for safety margin)
        """
        self.calls_per_minute = calls_per_minute
        self.call_times = []

    def wait_if_needed(self):
        """
        Check if we need to wait before making the next API call.
        If we've hit the rate limit, sleeps until we can make another call.
        """
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)

        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if t > one_minute_ago]

        # If we've hit the limit, wait until the oldest call is >1 minute old
        if len(self.call_times) >= self.calls_per_minute:
            oldest_call = self.call_times[0]
            sleep_time = 60 - (now - oldest_call).total_seconds()
            if sleep_time > 0:
                print(f"⏳ Rate limit reached. Waiting {sleep_time:.1f}s before next API call...")
                time.sleep(sleep_time + 0.5)  # Add small buffer

        # Record this call
        self.call_times.append(datetime.now())


MODEL = "gemini-2.0-flash-exp"

SVG_GENERATION_PROMPT = """You are an expert at creating educational diagrams in SVG format.

    Given an educational concept description, generate a clean, labeled SVG diagram suitable for students.

    CRITICAL REQUIREMENTS:
    1. Output ONLY valid SVG code (no markdown, no code blocks, no explanatory text)
    2. Start with <?xml version="1.0" encoding="UTF-8"?> and <svg xmlns="http://www.w3.org/2000/svg" ...>
    3. Use viewBox="0 0 512 512" for consistent sizing
    4. Include clear text labels using <text> elements
    5. Use arrows (<path> with markers or <polyline>) to show process flow
    6. Use high contrast colors (dark text/lines on white/light backgrounds)
    7. Use simple geometric shapes: <rect>, <circle>, <ellipse>, <path>, <line>, <polyline>
    8. Make text readable: font-size at least 14px, bold for headers
    9. Create textbook-style diagrams, not decorative art
    10. Ensure all text is horizontal and easy to read

    STYLE GUIDELINES:
    - Background: white or very light color (#FFFFFF or #F5F5F5)
    - Text: dark (#000000 or #333333), font-family="Arial, sans-serif"
    - Primary shapes: use educational colors (blue, green, orange) with good contrast
    - Borders: use stroke="#000000" or dark colors, stroke-width="2"
    - Labels: place near relevant shapes, use <text> with clear positioning
    - Arrows: solid lines with arrowheads, use <defs><marker> for arrow markers

    EXAMPLE STRUCTURE:
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
    <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#000" />
        </marker>
    </defs>

    <rect x="0" y="0" width="512" height="512" fill="#FFFFFF"/>

    <!-- Your diagram elements here -->
    <circle cx="100" cy="100" r="40" fill="#4A90E2" stroke="#000" stroke-width="2"/>
    <text x="100" y="105" text-anchor="middle" font-size="16" font-weight="bold" fill="#000">Label</text>

    <line x1="140" y1="100" x2="200" y2="100" stroke="#000" stroke-width="2" marker-end="url(#arrowhead)"/>
    </svg>

    Now generate the SVG diagram."""


def clean_svg_duplicate_attributes(svg_code: str) -> str:
    """
    Clean SVG code by removing duplicate attributes from elements.
    This fixes issues where AI generates elements with the same attribute multiple times.

    Args:
        svg_code: Raw SVG code string

    Returns:
        Cleaned SVG code string
    """
    try:
        # Use regex to find and fix duplicate attributes in SVG elements
        # Pattern: finds elements where an attribute appears multiple times

        def remove_duplicate_attrs(match):
            """Remove duplicate attributes from a single element"""
            element = match.group(0)

            # Extract all attributes
            attr_pattern = r'(\w+(?:-\w+)*)=["\']([^"\']*)["\']'
            attrs = re.findall(attr_pattern, element)

            # Keep only the last occurrence of each attribute
            seen_attrs = {}
            for attr_name, attr_value in attrs:
                seen_attrs[attr_name] = attr_value

            # Reconstruct element with unique attributes
            tag_match = re.match(r'<(\w+(?:-\w+)*)\s+', element)
            if tag_match:
                tag_name = tag_match.group(1)

                # Check if self-closing
                is_self_closing = element.rstrip().endswith('/>')

                # Rebuild element
                attrs_str = ' '.join([f'{k}="{v}"' for k, v in seen_attrs.items()])
                if is_self_closing:
                    return f'<{tag_name} {attrs_str}/>'
                else:
                    return f'<{tag_name} {attrs_str}>'

            return element

        # Apply to all opening tags with attributes
        cleaned_svg = re.sub(
            r'<(\w+(?:-\w+)*)\s+[^>]+/?>',
            remove_duplicate_attrs,
            svg_code
        )

        return cleaned_svg

    except Exception as e:
        print(f"Warning: Could not clean SVG attributes: {str(e)}")
        # Return original if cleaning fails
        return svg_code


def generate_svg_diagram(image_prompt: str, scene_id: int, rate_limiter: RateLimiter = None, max_retries: int = 3) -> str:
    """
    Generate SVG diagram with retry logic and exponential backoff.

    Args:
        image_prompt: Description of the diagram to generate
        scene_id: ID of the scene
        rate_limiter: Rate limiter instance
        max_retries: Maximum number of retry attempts on failure

    Returns:
        str: SVG code
    """
    for attempt in range(max_retries):
        try:
            # Wait if we're hitting rate limits
            if rate_limiter:
                rate_limiter.wait_if_needed()

            model = genai.GenerativeModel(
                model_name=MODEL,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                }
            )

            full_prompt = f"""{SVG_GENERATION_PROMPT}

        Create an educational diagram for this concept:
        {image_prompt}

        Remember:
        - Output ONLY the SVG code
        - Start with <?xml version="1.0" encoding="UTF-8"?>
        - Use viewBox="0 0 512 512"
        - Include clear labels using <text> elements
        - Use arrows to show relationships/flow
        - High contrast colors on white background
        - Make it look like a textbook diagram

        Generate the SVG now:"""

            response = model.generate_content(full_prompt)
            svg_code = response.text.strip()
            if svg_code.startswith("```svg"):
                svg_code = svg_code[6:]
            elif svg_code.startswith("```xml"):
                svg_code = svg_code[6:]
            elif svg_code.startswith("```"):
                svg_code = svg_code[3:]
            if svg_code.endswith("```"):
                svg_code = svg_code[:-3]

            svg_code = svg_code.strip()

            if not svg_code.startswith("<?xml") and not svg_code.startswith("<svg"): # sometimes the generated output can contain extra stuff so we first
            #search for where <xml> or <svg> begins and strip that part and then revuild structure. If not found, raise error.
                svg_match = re.search(r'<svg.*?</svg>', svg_code, re.DOTALL)
                if svg_match:
                    svg_code = svg_match.group(0)
                    svg_code = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_code
                else:
                    raise ValueError("Response does not contain valid SVG code")

            if "<svg" not in svg_code or "</svg>" not in svg_code:
                raise ValueError("Invalid SVG structure: missing <svg> tags")

            # Clean duplicate attributes that might cause parsing errors
            svg_code = clean_svg_duplicate_attributes(svg_code)

            print(f"Generated SVG for Scene {scene_id} ({len(svg_code)} chars)")
            return svg_code

        except Exception as e:
            # If this isn't the last attempt, retry with exponential backoff
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s, etc.
                print(f"⚠️  Error on attempt {attempt + 1}/{max_retries}: {str(e)}")
                print(f"⏳ Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                # Last attempt failed, raise the exception
                raise Exception(f"Failed to generate SVG for scene {scene_id} after {max_retries} attempts: {str(e)}")


def svg_to_png(svg_code: str, output_path: str, width: int = 512, height: int = 512):
    try:
        png_data = cairosvg.svg2png(
            bytestring=svg_code.encode('utf-8'), #svg is in string but cairosvg expects bytes so bytestring is used to convert str into bytes.
            output_width=width,
            output_height=height
        )

        image = Image.open(BytesIO(png_data))
        image.save(output_path, "PNG")

        print(f"Converted to PNG: {output_path}")

    except Exception as e:
        # Save the problematic SVG for debugging
        error_svg_path = output_path.replace('.png', '_error.svg')
        try:
            with open(error_svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_code)
            print(f"⚠️  Saved problematic SVG to: {error_svg_path}")
        except:
            pass

        error_msg = str(e)
        # Provide more helpful error messages
        if "duplicate attribute" in error_msg.lower():
            raise Exception(f"Failed to convert SVG to PNG - duplicate attribute detected: {error_msg}. Check {error_svg_path} for details.")
        else:
            raise Exception(f"Failed to convert SVG to PNG: {error_msg}")


def generate_images(script, output_dir="output_images"):
    os.makedirs(output_dir, exist_ok=True)
    results = []

    # Initialize rate limiter for image generation
    rate_limiter = RateLimiter(calls_per_minute=9)
    total_scenes = len(script["scenes"])

    print(f"\n🎨 Starting image generation for {total_scenes} scenes with rate limiting...")
    print(f"⚠️  This may take several minutes due to API rate limits (9 calls/min)\n")

    for scene in script["scenes"]:
        prompt = scene["image_prompt"]
        scene_id = scene["id"]

        print(f"\nGenerating educational diagram for Scene {scene_id}/{total_scenes}...")
        print(f"Prompt: {prompt}")

        try:
            svg_code = generate_svg_diagram(prompt, scene_id, rate_limiter)
            svg_path = os.path.join(output_dir, f"scene_{scene_id}.svg")
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_code)
            print(f"Saved SVG: {svg_path}")

            png_path = os.path.join(output_dir, f"scene_{scene_id}.png")
            svg_to_png(svg_code, png_path, width=512, height=512)

            results.append(png_path)
            print(f"Completed Scene {scene_id}")

        except Exception as e:
            print(f"Error generating diagram for Scene {scene_id}: {str(e)}")
            raise Exception(f"Failed to generate diagram for scene {scene_id}: {str(e)}")

    return results

#Earlier openai api was used hence generate_image function is aliased as previously used function name so that it doesn't break the code.
generate_images_dalle2 = generate_images
