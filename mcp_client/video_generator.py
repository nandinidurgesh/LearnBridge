import os
from pathlib import Path
import subprocess
from datetime import datetime

class VideoGenerator:

    def __init__(self, output_dir="videos"):
        """Initialize video generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp_audio_files")
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate_speech(self, text: str, audio_file: str) -> bool:
        """Generate speech from text using gTTS"""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(audio_file)
            print(f"✓ Speech generated: {audio_file}")
            return True
        except Exception as e:
            print(f"✗ Speech generation failed: {e}")
            return False

    def create_html_video(self, text: str, audio_file: str, output_html: str) -> bool:
        """Create HTML file with embedded audio"""
        try:
            import shutil
            from pathlib import Path
            import json
            # Copy audio file to same folder as HTML
            output_path = Path(output_html)
            audio_filename = Path(audio_file).name
            audio_copy = output_path.parent / audio_filename
            shutil.copy(audio_file, audio_copy)
            
            # Split text into sentences
            sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
            sentences_json = json.dumps(sentences)
            
            # Build HTML separately to avoid f-string escaping issues
            html_head = """<!DOCTYPE html>
            <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>LearnBridge Video</title> <style> * { margin: 0; padding: 0; box-sizing: border-box; } body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; } .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); max-width: 900px; width: 100%; } h1 { color: #667eea; text-align: center; margin-bottom: 30px; font-size: 28px; } #canvas { border: 3px solid #667eea; display: block; margin: 20px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; width: 100%; height: auto; } #audioContainer { margin: 20px 0; } audio { width: 100%; outline: none; } .text-display { background: #f8f9fa; padding: 25px; border-radius: 10px; font-size: 17px; line-height: 1.8; color: #333; min-height: 120px; } .sentence { opacity: 0.3; transition: opacity 0.3s ease-in; display: inline; } .sentence.active { opacity: 1; font-weight: bold; color: #667eea; } </style> </head> <body> <div class="container"> <h1>🎓 LearnBridge - Interactive Learning</h1> <canvas id="canvas" width="900" height="300"></canvas> <div id="audioContainer"> <audio id="audio" controls> <source src="AUDIO_FILE_PLACEHOLDER" type="audio/mpeg"> Your browser does not support the audio element. </audio> </div> <div class="text-display" id="textDisplay"> <p id="sentenceContainer"></p> </div> </div> <script> const canvas = document.getElementById('canvas'); const ctx = canvas.getContext('2d'); const audio = document.getElementById('audio'); const sentenceContainer = document.getElementById('sentenceContainer');
                const sentences = SENTENCES_PLACEHOLDER;
        
            let animationFrames = 0;
            
            function drawFrame() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Draw title
                ctx.fillStyle = '#667eea';
                ctx.font = 'bold 28px Arial';
                ctx.fillText('📚 Learning Content', 50, 50);
                
                // Draw progress bar background
                ctx.fillStyle = '#e0e0e0';
                ctx.fillRect(50, 80, 800, 12);
                
                // Draw progress bar foreground
                const progress = audio.duration ? audio.currentTime / audio.duration : 0;
                ctx.fillStyle = '#667eea';
                ctx.fillRect(50, 80, 800 * progress, 12);
                
                // Draw time
                const currentMin = Math.floor(audio.currentTime / 60);
                const currentSec = Math.floor(audio.currentTime % 60);
                const totalMin = Math.floor(audio.duration / 60);
                const totalSec = Math.floor(audio.duration % 60);
                
                ctx.fillStyle = '#333';
                ctx.font = '16px Arial';
                ctx.fillText(
                    currentMin + ':' + String(currentSec).padStart(2, '0') + ' / ' + totalMin + ':' + String(totalSec).padStart(2, '0'),
                    50,
                    120
                );
                
                // Draw animated circles
                ctx.fillStyle = '#764ba2';
                for(let i = 0; i < 3; i++) {
                    const x = 200 + i * 120;
                    const y = 200 + Math.sin(animationFrames * 0.1 + i) * 40;
                    ctx.beginPath();
                    ctx.arc(x, y, 20, 0, 2 * Math.PI);
                    ctx.fill();
                }
                
                animationFrames++;
                requestAnimationFrame(drawFrame);
            }
            
            // Update text based on audio progress
            audio.addEventListener('timeupdate', function() {
                if(!this.duration) return;
                
                const currentTime = this.currentTime;
                const audioPercentage = currentTime / this.duration;
                const sentenceIndex = Math.floor(audioPercentage * sentences.length);
                
                let html = '';
                sentences.forEach((sentence, index) => {
                    const className = index < sentenceIndex ? 'sentence active' : 'sentence';
                    html += '<span class="' + className + '">' + sentence + ' </span>';
                });
                sentenceContainer.innerHTML = html;
            });
            
            drawFrame();
            </script>

            </body> </html>"""

            # Replace placeholders
            html_content = html_head.replace('AUDIO_FILE_PLACEHOLDER', audio_filename)
            html_content = html_content.replace('SENTENCES_PLACEHOLDER', sentences_json)
            
            with open(output_html, 'w') as f:
                f.write(html_content)
            
            print(f"✓ HTML created: {output_html}")
            print(f"✓ Audio copied: {audio_copy}")
            return True
        except Exception as e:
            print(f"✗ HTML creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False


    def create_video(self, text: str, question: str = "Question") -> str:
        """Create audio + HTML for interactive learning"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = self.temp_dir / f"audio_{timestamp}.mp3"
            html_file = self.output_dir / f"video_{timestamp}.html"
            
            print("\n🎬 Creating interactive video...")
            print(f"   Question: {question}")
            
            # Step 1: Generate speech
            print("   1. Generating speech...")
            if not self.generate_speech(text, str(audio_file)):
                return None
            
            # Step 2: Create HTML with canvas animation
            print("   2. Creating interactive HTML...")
            if not self.create_html_video(text, str(audio_file), str(html_file)):
                return None
            
            print(f"✓ Video created: {html_file}")
            return str(html_file)
        
        except Exception as e:
            print(f"✗ Video creation failed: {e}")
            return None
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except:
            pass