# 🤖 A² — Personal AI Assistant

A fully local, voice-activated AI assistant that runs 100% on your laptop. No API keys. No cloud. No cost.

Just say **"Hey A²"** and it wakes up, recognizes your voice, and responds instantly.

## ✨ Features
- 🎙️ Wake word activation — say "Hey A²" to activate
- 🔐 Voice recognition — only responds to your voice
- 💬 Gen Z personality — casual, funny, actually helpful
- 🌐 Opens apps and websites by voice command
- 🔍 Searches Google hands free
- 🧠 Remembers full conversation history
- 🖥️ Animated orb that reacts in real time
- 🚀 Starts automatically on laptop startup
- ⚡ Runs 100% locally — no internet needed for AI

## 🛠️ Tech Stack
- Python
- Ollama + Llama 3.2 — local AI model
- SpeechRecognition — voice input
- pyttsx3 — text to speech
- CustomTkinter — desktop UI
- NumPy — voice recognition
- PyAudio — microphone access

## 💻 Hardware Used
- NVIDIA GeForce RTX 3060 Laptop GPU
- Runs completely offline

## 🚀 How to Run
1. Install Ollama from ollama.com and run `ollama pull llama3.2`
2. Install dependencies:
pip install ollama speechrecognition pyttsx3 pyaudio customtkinter numpy
3. Enroll your voice:
python enrollVoice.py
4. Run the assistant:
python assistant.py
5. Say **"Hey A²"** to wake it up!

## 🗣️ Voice Commands
- "Open YouTube" — opens YouTube
- "Open Spotify" — opens Spotify
- "Search for Python tutorials" — searches Google
- "What time is it?" — tells the time
- "Open VS Code" — opens VS Code
- Any question — answered by Llama 3.2 AI

## 💡 Auto Start on Windows
Add `launch.vbs` to your Windows startup folder to have A² start automatically every time you turn on your laptop.
