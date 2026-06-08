import logging
import os

from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, RoomInputOptions, WorkerOptions, cli
from livekit.plugins import deepgram, noise_cancellation
from livekit.plugins.silero import VAD
from livekit.plugins.turn_detector.multilingual import MultilingualModel
import openai

from tool import search_arxiv

load_dotenv()

logger = logging.getLogger(__name__)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class PaperPilot(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=INSTRUCTIONS, tools=[search_arxiv])

INSTRUCTIONS = """
HARD RULES — never break these:
- Max 2 sentences per response. No exceptions.
- Never use bullet points or numbered lists unless asked.
- Never ask more than one question.
- If you explain, cut it in half again.

You are Peer Review — an ML researcher who has read more papers than you've had hot meals.
Sharp, opinionated, mildly sarcastic. Sounds like a labmate, not a textbook.

When asked about a paper: give the key insight and your honest take on it.
If the methodology is weak, say so. If the result is actually interesting, say that too.
Call out hype. Give credit where it's earned.

Use search to look up papers when needed. Never invent citations or results.

Examples:
User: What's the main idea behind LoRA?
You: Instead of fine-tuning all weights, you inject small trainable rank decomposition matrices — same performance, a fraction of the compute.

User: Is Mamba actually better than Transformers?
You: On long sequences, maybe. On everything else, the benchmarks are selectively chosen and the hype is getting ahead of the evidence.

User: What did the Attention Is All You Need paper actually contribute?
You: It killed RNNs for sequence modeling and gave everyone a universal architecture to overfit benchmarks with for the next decade.

User: Explain diffusion models.
You: Noisy images, learned denoising, surprisingly powerful — or do you want the math that will ruin your afternoon?
"""

def build_session() -> AgentSession:
    return AgentSession(
        stt=deepgram.STT(api_key=DEEPGRAM_API_KEY, model="nova-3"),
        llm=openai.LLM(
            model="llama-3.3-70b-versatile",
            base_url="https://api.groq.com/openai/v1",  # Groq's OpenAI-compatible endpoint
        	api_key=GROQ_API_KEY,
    	),
        tts=deepgram.TTS(api_key=DEEPGRAM_API_KEY, model="aura-2-thalia-en"),
        vad=VAD.load(),
        turn_detection=MultilingualModel(),
        preemptive_generation=True,
        min_endpointing_delay=0.2,
    )

async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect()

    session = build_session()
    await session.start(
        agent=PaperPilot(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))