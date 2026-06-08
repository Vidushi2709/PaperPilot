# PaperPilot

A real-time voice AI research agent that listens to your questions about ML papers, responds conversationally, and can fetch relevant research from arXiv.

It’s built using LiveKit for real-time audio, Deepgram for speech I/O, and Groq-hosted LLMs for reasoning.

---

## 🧠 What this does

PaperPilot is a voice-based research assistant that:

* Converts speech → text (Deepgram STT)
* Thinks using an LLM (Groq / Llama)
* Responds via voice (Deepgram TTS)
* Can fetch papers from arXiv when needed
* Runs in real-time via LiveKit

It is designed to behave like a research peer rather than a passive assistant.

---

## 📁 Project Structure

```
paperpilot/
├── agent.py          # Core voice agent logic
├── tool.py           # arXiv search tool
├── requirements.txt  # Dependencies
├── .env              # API keys (not committed)
├── prompts/          # System prompt variants
│   ├── skeptic.txt
│   ├── professor.txt
│   ├── rubber_duck.txt
│   └── chaos.txt
├── .gitignore
```

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/Vidushi2709/PaperPilot.git
cd PaperPilot
```

---

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add environment variables

Create a `.env` file:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
```

---

## 🚀 Run locally

```bash
python agent.py console
```

This starts a local LiveKit session where you can talk to the agent.

---

## 🔍 Tooling

### arXiv search

The agent has access to a tool that queries arXiv:

* Searches latest research papers
* Returns titles, authors, abstracts, and links
* Used when the model decides it needs external evidence

Defined in: `tool.py`

---

## 🧩 Core Components

### STT (Speech-to-Text)

* Deepgram `nova-3`

### LLM

* Groq API (Llama 3.3 70B / compatible models)

### TTS (Text-to-Speech)

* Deepgram `aura-2-thalia-en`

### Voice Layer

* LiveKit Agents framework
* Silero VAD for speech detection
* Noise cancellation enabled

---

## 🧪 Prompts

Different system prompt styles are included in `/prompts`:

* `skeptic.txt` → critical research peer
* `professor.txt` → structured academic tone
* `rubber_duck.txt` → neutral debugging assistant
* `chaos.txt` → experimental / unpredictable mode

---

## 🧠 Design Goal

It is a **real-time research companion** that:

* challenges weak assumptions
* pulls in papers when needed
* avoids hallucinated citations
* responds in natural conversation

---

## 🧪 Example questions

* “What are the latest benchmarks for LLM reasoning?”
* “Is LoRA still relevant compared to full fine-tuning?”
* “What did the Mamba paper actually improve over Transformers?”
* “Find recent papers on multimodal agents”

---

## 📦 Requirements

See `requirements.txt`

Main dependencies:

* livekit-agents
* livekit-plugins-deepgram
* livekit-plugins-silero
* livekit-turn-detector
* httpx
* python-dotenv
