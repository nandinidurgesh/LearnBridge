import asyncio
import sys
from pathlib import Path

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from video_generator import VideoGenerator


class LearnBridgeAgent:
    def __init__(self):
        self.agent = None
        self.llm = None
        self.tools = None
        self.video_generator = VideoGenerator()

    async def setup(self):
        """Setup agent with Wikipedia tool"""
        print("Setting up LearnBridge Agent...")
        try:
            print("Loading Wikipedia tool...")
            wikipedia_tool = WikipediaQueryRun(
                api_wrapper=WikipediaAPIWrapper()
            )
            self.tools = [wikipedia_tool]
            print("Connecting to Ollama...")
            self.llm = ChatOllama(
                model="mistral",
                base_url="http://localhost:11434",
                temperature=0.7
            )
            print("Creating agent...")
            self.agent = create_react_agent(
                self.llm,
                self.tools
            )
            print("✓ Agent ready!")
            print("✓ Video generation ready!")
        except Exception as e:
            print(f"✗ Setup failed: {e}")
            import traceback
            traceback.print_exc()
            raise

    async def ask(self, question: str) -> str:
        """Answer a question"""
        if self.agent is None:
            raise RuntimeError("Agent not initialized. Call setup() first.")
        try:
            response = await self.agent.ainvoke({
                'messages': [{'role': 'user', 'content': question}]
            })
            return response['messages'][-1].content
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"

    def generate_video(self, answer: str, question: str) -> str:
        """Generate video from answer"""
        try:
            video_path = self.video_generator.create_video(answer, question)
            return video_path
        except Exception as e:
            print(f"✗ Video generation error: {e}")
            return None


async def main():
    """Main CLI loop"""
    agent = LearnBridgeAgent()
    await agent.setup()

    print("\n" + "=" * 60)
    print("LearnBridge - Educational AI Tutor with Video")
    print("=" * 60)
    print("Ask educational questions. Type 'quit' to exit.")
    print("Type 'video' to generate video for last answer.\n")
    last_answer = None
    last_question = None

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() == 'quit':
                print("Goodbye!")
                agent.video_generator.cleanup()
                break
            if user_input.lower() == 'video':
                if last_answer and last_question:
                    print("\n🎬 Generating video for last answer...")
                    video_path = agent.generate_video(last_answer, last_question)
                    if video_path:
                        print(f"✓ Video saved to: {video_path}\n")
                    else:
                        print("✗ Video generation failed\n")
                else:
                    print("No previous answer to convert to video.\n")
                continue
            if not user_input:
                continue
            print("Thinking...\n")
            answer = await agent.ask(user_input)
            print(f"LearnBridge: {answer}\n")
            last_answer = answer
            last_question = user_input
            print("💡 Tip: Type 'video' to generate a video of this answer.\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            agent.video_generator.cleanup()
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
