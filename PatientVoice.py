import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get API Key from Environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as an MP3 file.

    Args:
    - file_path (str): Path to save the recorded audio file.
    - timeout (int): Max wait time for speech (in seconds).
    - phrase_time_limit (int): Max duration for speech recording (in seconds).
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert recorded audio to MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording: {e}")


def transcribe_with_groq(stt_model, audio_filepath):
    """
    Transcribes an audio file using the Groq Whisper STT model.

    Args:
    - stt_model (str): The speech-to-text model to use.
    - audio_filepath (str): Path to the audio file.

    Returns:
    - str: Transcription text or error message.
    """
    if not os.path.exists(audio_filepath):
        logging.error(f"Error: File {audio_filepath} not found.")
        return None

    try:
        client = Groq(api_key=GROQ_API_KEY)

        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )

           

            return transcription.text

    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return None


# Main Execution
if __name__ == "__main__":
    audio_filepath = "patient_voice_test_for_patient.mp3"
    # record_audio(file_path=audio_filepath)

    # Run transcription
    stt_model = "whisper-large-v3"
    result = transcribe_with_groq(stt_model, audio_filepath)

    if result:
        print(result)
    else:
        print("\nTranscription failed.")
