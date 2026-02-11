import os
import platform
import subprocess
from gtts import gTTS
from elevenlabs.client import ElevenLabs

# -------------------------------
# PLAY AUDIO CROSS-PLATFORM
# -------------------------------
def play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":
            # Use default media player
            subprocess.run(['start', '', filepath], shell=True)
        elif os_name == "Linux":
            # Make sure 'mpg123' is installed, or use 'aplay' for wav
            subprocess.run(['mpg123', filepath])
        else:
            print("Unsupported OS. Audio saved but not played.")
    except Exception as e:
        print(f"Error playing audio: {e}")

# -------------------------------
# gTTS TEXT TO SPEECH
# -------------------------------
def text_to_speech_with_gtts(input_text, output_filepath):
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(output_filepath)
    print(f"gTTS audio saved: {output_filepath}")
    play_audio(output_filepath)

# -------------------------------
# ELEVENLABS TEXT TO SPEECH
# -------------------------------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    voice_id = "EXAVITQu4vr4xnSDxMaL"  # Default Sarah voice

    # Convert text to speech (returns generator)
    audio_generator = client.text_to_speech.convert(
        text=input_text,
        voice_id=voice_id,
        model_id="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )

    # Save generator output to file
    with open(output_filepath, "wb") as f:
        for chunk in audio_generator:
            f.write(chunk)

    print(f"ElevenLabs audio saved: {output_filepath}")
    play_audio(output_filepath)

# -------------------------------
# MAIN PROGRAM
# -------------------------------
if __name__ == "__main__":
    input_text = "Hello, I am your AI doctor. Please describe your symptoms."

    # Generate gTTS audio
    text_to_speech_with_gtts(input_text, "doctor_voice_gtts.mp3")

    # Generate ElevenLabs audio
    text_to_speech_with_elevenlabs(input_text, "doctor_voice_elevenlabs.mp3")
