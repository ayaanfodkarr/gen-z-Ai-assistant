import ollama
import speech_recognition as sr
import pyttsx3
import customtkinter as ctk
import threading
import math
import numpy as np
import pickle
import os
import subprocess
import webbrowser
import datetime
from tkinter import Canvas

# ============================================
# CONFIGURATION
# ============================================
ASSISTANT_NAME = "A\u00b2"
WAKE_WORDS = ["hey a square", "hey square", "hey a squared", "hey squared"]
YOUR_NAME = "Ayaan"
PERSONALITY = """
You are A², Ayaan's personal AI assistant with a Gen Z personality.
- You're cool, casual and funny
- You use Gen Z slang naturally (no cap, lowkey, bussin, fr fr, slay etc.)
- You keep answers short and punchy — no long boring paragraphs
- You call the user Ayaan
- You're confident and a bit sarcastic but always helpful
- You never say you're an AI unless asked
- You're like that one smart friend who knows everything
"""

# ============================================
# VOICE PROFILE
# ============================================
def load_voice_profile():
    try:
        with open(r'C:\Users\Ayaan\gen-z-assistant\voice_profile.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

def get_voice_signature(audio_data):
    samples = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16).astype(np.float32)
    energy = np.sqrt(np.mean(samples**2))
    zero_crossings = np.sum(np.abs(np.diff(np.sign(samples)))) / len(samples)
    fft = np.abs(np.fft.rfft(samples))
    fft_normalized = fft / (np.sum(fft) + 1e-10)
    freqs = np.arange(len(fft_normalized))
    centroid = np.sum(freqs * fft_normalized)
    spread = np.sqrt(np.sum(((freqs - centroid)**2) * fft_normalized))
    band_size = max(1, len(fft) // 10)
    bands = [np.mean(fft[i*band_size:(i+1)*band_size]) for i in range(10)]
    bands = np.array(bands) / (np.max(bands) + 1e-10)
    return np.array([energy, zero_crossings, centroid, spread] + list(bands))

def verify_voice(audio_data, profile, threshold=15.0):
    if profile is None:
        return True
    try:
        sig = get_voice_signature(audio_data)
        diff = np.abs(sig - profile['mean']) / profile['std']
        score = np.mean(diff)
        print(f"Voice match score: {score:.2f} (lower = better)")
        return score < threshold
    except:
        return True

# ============================================
# ACTIONS
# ============================================
def execute_action(command):
    """Detects and executes actions from voice commands"""
    c = command.lower()

    # YouTube
    if 'youtube' in c:
        webbrowser.open('https://youtube.com')
        return "Opening YouTube, no cap! \U0001f3a5"

    # Google search
    elif 'search for' in c or 'search' in c:
        query = c.replace('search for', '').replace('search', '').strip()
        if query:
            webbrowser.open(f'https://google.com/search?q={query}')
            return f"Searching for {query}, bestie! \U0001f50d"
        else:
            webbrowser.open('https://google.com')
            return "Google is up! \U0001f50d"

    # Google
    elif 'open google' in c or c == 'google':
        webbrowser.open('https://google.com')
        return "Google opened, slay! \U0001f50d"

    # Instagram
    elif 'instagram' in c:
        webbrowser.open('https://instagram.com')
        return "Instagram loading! \U0001f4f8"

    # Spotify web
    elif 'spotify' in c:
        webbrowser.open('https://open.spotify.com')
        return "Spotify opening, let's vibe! \U0001f3b5"

    # Netflix
    elif 'netflix' in c:
        webbrowser.open('https://netflix.com')
        return "Netflix and chill incoming! \U0001f3ac"

    # GitHub
    elif 'github' in c:
        webbrowser.open('https://github.com/ayaanfodkarr')
        return "Your GitHub is open, king! \U0001f468\u200d\U0001f4bb"

    # LinkedIn
    elif 'linkedin' in c:
        webbrowser.open('https://linkedin.com')
        return "LinkedIn loading, time to network! \U0001f4bc"

    # WhatsApp
    elif 'whatsapp' in c:
        webbrowser.open('https://web.whatsapp.com')
        return "WhatsApp Web opening! \U0001f4ac"

    # Calculator
    elif 'calculator' in c:
        subprocess.Popen(['calc.exe'])
        return "Calculator opened! \U0001f522"

    # Notepad
    elif 'notepad' in c:
        subprocess.Popen(['notepad.exe'])
        return "Notepad opened! \U0001f4dd"

    # File explorer
    elif 'file explorer' in c or 'my files' in c or 'explorer' in c:
        subprocess.Popen(['explorer.exe'])
        return "File explorer opened! \U0001f4c1"

    # VS Code
    elif 'vs code' in c or 'vscode' in c or 'visual studio' in c:
        try:
            subprocess.Popen(['code'])
        except:
            subprocess.Popen(['C:\\Users\\Ayaan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'])
        return "VS Code opening, let's code! \U0001f4bb"

    # Chrome
    elif 'chrome' in c:
        try:
            subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])
        except:
            webbrowser.open('https://google.com')
        return "Chrome opening! \U0001f310"

    # Time
    elif 'time' in c and ('what' in c or 'current' in c):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"It's {now}, bestie! \u23f0"

    # Date
    elif 'date' in c or 'today' in c or 'what day' in c:
        today = datetime.datetime.now().strftime("%A, %B %d %Y")
        return f"Today is {today}, no cap! \U0001f4c5"

    # Shutdown
    elif 'shutdown' in c or 'shut down' in c:
        os.system('shutdown /s /t 5')
        return "Shutting down in 5 seconds! Bye Ayaan! \U0001f44b"

    # Restart
    elif 'restart' in c:
        os.system('shutdown /r /t 5')
        return "Restarting in 5 seconds! \U0001f504"

    # No action found — let AI handle it
    return None

# ============================================
# SPEECH ENGINE
# ============================================
def setup_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    return engine

def speak(text):
    print(f"\n\U0001f916 A²: {text}\n")
    try:
        engine = setup_voice()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio).lower()
            print(f"\U0001f3a4 You said: {text}")
            return text
        except:
            return ""

def think(prompt, conversation_history):
    messages = [{'role': 'system', 'content': PERSONALITY}]
    messages.extend(conversation_history)
    messages.append({'role': 'user', 'content': prompt})
    response = ollama.chat(model='llama3.2', messages=messages)
    return response['message']['content']

# ============================================
# ANIMATED ORB
# ============================================
class AnimatedOrb:
    def __init__(self, canvas, cx, cy, radius):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.state = "idle"
        self.angle = 0
        self.pulse = 0
        self.animate()

    def set_state(self, state):
        self.state = state

    def draw(self):
        self.canvas.delete("orb")

        if self.state == "idle":
            core_color = "#1a1a2e"
            glow_color = "#0066ff"
            ring_color = "#0044cc"
        elif self.state == "listening":
            core_color = "#1a2e1a"
            glow_color = "#00ff88"
            ring_color = "#00cc66"
        elif self.state == "thinking":
            core_color = "#2e1a1a"
            glow_color = "#ff6600"
            ring_color = "#cc4400"
        elif self.state == "speaking":
            core_color = "#1a1a2e"
            glow_color = "#aa00ff"
            ring_color = "#8800cc"

        self.pulse += 0.05
        pulse_size = math.sin(self.pulse) * 10

        for i in range(4, 0, -1):
            size = self.radius + pulse_size + (i * 15)
            self.canvas.create_oval(
                self.cx - size, self.cy - size,
                self.cx + size, self.cy + size,
                fill="", outline=glow_color,
                width=2, tags="orb"
            )

        r = self.radius + pulse_size
        self.canvas.create_oval(
            self.cx - r, self.cy - r,
            self.cx + r, self.cy + r,
            fill=core_color, outline=glow_color,
            width=3, tags="orb"
        )

        self.angle += 2
        for i in range(8):
            angle_rad = math.radians(self.angle + i * 45)
            x = self.cx + (r + 20) * math.cos(angle_rad)
            y = self.cy + (r + 20) * math.sin(angle_rad)
            dot_size = 4 if i % 2 == 0 else 2
            self.canvas.create_oval(
                x - dot_size, y - dot_size,
                x + dot_size, y + dot_size,
                fill=ring_color, outline="", tags="orb"
            )

        inner_r = r * 0.6
        self.canvas.create_oval(
            self.cx - inner_r, self.cy - inner_r,
            self.cx + inner_r, self.cy + inner_r,
            fill=glow_color, outline="", tags="orb"
        )

        core_r = r * 0.2
        self.canvas.create_oval(
            self.cx - core_r, self.cy - core_r,
            self.cx + core_r, self.cy + core_r,
            fill="white", outline="", tags="orb"
        )

    def animate(self):
        self.draw()
        self.canvas.after(30, self.animate)


# ============================================
# MAIN APP
# ============================================
class AssistantUI:
    def __init__(self):
        self.conversation_history = []
        self.is_running = True

        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("A\u00b2 \u2014 Personal AI Assistant")
        self.root.geometry("480x800")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#000000")

        self.build_ui()
        self.start_wake_word_listener()

    def build_ui(self):
        title = ctk.CTkLabel(
            self.root,
            text="A\u00b2",
            font=ctk.CTkFont(size=52, weight="bold"),
            text_color="#0066ff"
        )
        title.pack(pady=(30, 0))

        subtitle = ctk.CTkLabel(
            self.root,
            text="Personal AI Assistant",
            font=ctk.CTkFont(size=13),
            text_color="#444"
        )
        subtitle.pack()

        self.canvas = Canvas(
            self.root,
            width=480,
            height=280,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.orb = AnimatedOrb(self.canvas, 240, 140, 80)

        self.status_label = ctk.CTkLabel(
            self.root,
            text='Say "Hey A\u00b2" to wake me up',
            font=ctk.CTkFont(size=13),
            text_color="#444"
        )
        self.status_label.pack(pady=5)

        self.chat_display = ctk.CTkTextbox(
            self.root,
            width=440,
            height=200,
            font=ctk.CTkFont(size=12),
            corner_radius=15,
            fg_color="#0a0a0a",
            text_color="#cccccc",
            border_color="#222",
            border_width=1
        )
        self.chat_display.pack(pady=10, padx=20)
        self.chat_display.insert("end", "A\u00b2: Yo Ayaan! \U0001f44b Say 'Hey A\u00b2' to get started, no cap!\n\n")
        self.chat_display.configure(state="disabled")

        input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        input_frame.pack(pady=5, padx=20, fill="x")

        self.text_input = ctk.CTkEntry(
            input_frame,
            height=45,
            placeholder_text="Or type here and press Enter...",
            font=ctk.CTkFont(size=13),
            corner_radius=15,
            fg_color="#0a0a0a",
            border_color="#222",
            text_color="white"
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.text_input.bind("<Return>", self.handle_text_input)

        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            width=80,
            height=45,
            corner_radius=15,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.handle_text_input
        )
        send_btn.pack(side="right")

    def update_status(self, text, color="#444"):
        self.status_label.configure(text=text, text_color=color)

    def add_message(self, sender, message):
        self.chat_display.configure(state="normal")
        if sender == "You":
            self.chat_display.insert("end", f"\U0001f464 You: {message}\n\n")
        else:
            self.chat_display.insert("end", f"\U0001f916 A\u00b2: {message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def process_input(self, user_input):
        if not user_input.strip():
            return

        for word in WAKE_WORDS:
            user_input = user_input.replace(word, "").strip()

        if not user_input:
            return

        print(f"Sending to AI: {user_input}")
        self.add_message("You", user_input)
        self.orb.set_state("thinking")
        self.root.after(0, lambda: self.update_status("\U0001f4ad Thinking...", "#ff6600"))

        def get_response():
            # Check for actions first
            action_response = execute_action(user_input)
            if action_response:
                response = action_response
            else:
                response = think(user_input, self.conversation_history)

            print(f"Response: {response}")
            self.conversation_history.append({'role': 'user', 'content': user_input})
            self.conversation_history.append({'role': 'assistant', 'content': response})

            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            self.root.after(0, lambda: self.add_message("A\u00b2", response))
            self.orb.set_state("speaking")
            self.root.after(0, lambda: self.update_status("\U0001f50a Speaking...", "#aa00ff"))

            def do_speak():
                speak(response)
                self.orb.set_state("idle")
                self.root.after(0, lambda: self.update_status('Say "Hey A\u00b2" to wake me up', "#444"))

            threading.Thread(target=do_speak, daemon=True).start()

        threading.Thread(target=get_response, daemon=True).start()

    def handle_text_input(self, event=None):
        user_input = self.text_input.get()
        self.text_input.delete(0, "end")
        self.process_input(user_input)

    def show_window(self):
        self.root.deiconify()
        self.root.state('normal')
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()

    def start_wake_word_listener(self):
        def wake_word_loop():
            voice_profile = load_voice_profile()
            print(f"Voice profile loaded: {voice_profile is not None}")

            while self.is_running:
                try:
                    recognizer = sr.Recognizer()
                    recognizer.energy_threshold = 300
                    recognizer.dynamic_energy_threshold = True
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        audio = recognizer.listen(source, timeout=4, phrase_time_limit=6)
                    try:
                        text = recognizer.recognize_google(audio).lower()
                        print(f"Heard: {text}")

                        is_your_voice = verify_voice(audio, voice_profile)

                        if any(word in text for word in WAKE_WORDS) and is_your_voice:
                            print("✅ Wake word detected — voice verified!")
                            self.root.after(0, self.show_window)
                            self.orb.set_state("listening")
                            self.root.after(0, lambda: self.update_status("\U0001f442 Listening...", "#00ff88"))

                            command = text
                            for word in WAKE_WORDS:
                                command = command.replace(word, "").strip()

                            if command and len(command) > 2:
                                print(f"Command from same phrase: {command}")
                                self.root.after(0, lambda c=command: self.process_input(c))
                            else:
                                print("Waiting for command...")
                                command = listen()
                                if command:
                                    self.root.after(0, lambda c=command: self.process_input(c))
                                else:
                                    self.orb.set_state("idle")
                                    self.root.after(0, lambda: self.update_status('Say "Hey A\u00b2" to wake me up', "#444"))
                        elif any(word in text for word in WAKE_WORDS) and not is_your_voice:
                            print("❌ Wake word detected but voice not recognized!")
                    except:
                        pass
                except:
                    pass

        threading.Thread(target=wake_word_loop, daemon=True).start()

    def run(self):
        self.root.withdraw()

        def startup_speak():
            speak("Yo Ayaan! A square is online in the background, no cap. Say Hey A square whenever you need me!")
        threading.Thread(target=startup_speak, daemon=True).start()
        self.root.mainloop()


# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    app = AssistantUI()
    app.run()