import speech_recognition as sr
import numpy as np
import pickle
import os

def get_voice_signature(audio_data):
    """Extract voice signature from audio"""
    samples = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16).astype(np.float32)
    
    # Extract features
    energy = np.sqrt(np.mean(samples**2))
    zero_crossings = np.sum(np.abs(np.diff(np.sign(samples)))) / len(samples)
    
    # Frequency features using FFT
    fft = np.abs(np.fft.rfft(samples))
    fft_normalized = fft / (np.sum(fft) + 1e-10)
    
    # Spectral centroid
    freqs = np.arange(len(fft_normalized))
    centroid = np.sum(freqs * fft_normalized)
    
    # Spectral spread
    spread = np.sqrt(np.sum(((freqs - centroid)**2) * fft_normalized))
    
    # Top frequency bands
    band_size = len(fft) // 10
    bands = [np.mean(fft[i*band_size:(i+1)*band_size]) for i in range(10)]
    bands = np.array(bands) / (np.max(bands) + 1e-10)
    
    signature = np.array([energy, zero_crossings, centroid, spread] + list(bands))
    return signature

def enroll_voice():
    print("🎙️ Voice Enrollment for A²")
    print("=" * 40)
    print("I'll record your voice 5 times.")
    print("Each time say: 'Hey A square'\n")
    
    recognizer = sr.Recognizer()
    signatures = []
    
    for i in range(5):
        input(f"Press Enter and say 'Hey A square' (sample {i+1}/5)...")
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🔴 Recording...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                sig = get_voice_signature(audio)
                signatures.append(sig)
                print(f"✅ Sample {i+1} recorded!\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    if len(signatures) >= 3:
        # Save voice profile
        voice_profile = {
            'mean': np.mean(signatures, axis=0),
            'std': np.std(signatures, axis=0) + 1e-10
        }
        
        with open('voice_profile.pkl', 'wb') as f:
            pickle.dump(voice_profile, f)
        
        print("✅ Voice profile saved!")
        print("A² will now only respond to your voice!")
    else:
        print("❌ Not enough samples. Please try again.")

if __name__ == "__main__":
    enroll_voice()