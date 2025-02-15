import os
import subprocess
import platform
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    
    # Generate MP3 file
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Convert MP3 to WAV
    wav_filepath = output_filepath.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-i", output_filepath, wav_filepath, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Play the audio based on OS
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", wav_filepath])
        elif os_name == "Windows":  # Windows (using PowerShell)
            subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(["aplay", wav_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Test the function
input_text = "Code is running!"
text_to_speech_with_gtts(input_text, output_filepath="gtts_testing_autoplay.mp3")
