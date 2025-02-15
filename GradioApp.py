from DoctorBrain import encode_image, analyze_image_with_query
from PatientVoice import record_audio, transcribe_with_groq
from DoctorVoice import text_to_speech_with_gtts
import gradio as gr
import os

# Hardcoded API Key
GROQ_API_KEY = "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"

# System Prompt
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    try:
        # Step 1: Convert Speech to Text
        print("Transcribing audio...")
        speech_to_text_output = transcribe_with_groq(
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        print("Transcription:", speech_to_text_output)

        # Step 2: Analyze Image with AI Model
        doctor_response = "No image provided for analysis."
        if image_filepath:
            print("Encoding and analyzing image...")
            encoded_image = encode_image(image_filepath)
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encoded_image,
                model="llama-3.2-11b-vision-preview"
            )
        print("Doctor's response:", doctor_response)

        # Step 3: Convert Text to Speech
        output_audio_path = "final.mp3"
        print("Generating voice response...")
        text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_path)
        print("Voice response saved as:", output_audio_path)

        return speech_to_text_output, doctor_response, output_audio_path
    
    except Exception as e:
        print("Error occurred:", str(e))
        return "Error in processing audio/image", "Error occurred", None


# Create the Gradio Interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice")
    ],
    title="AI Doctor with Vision and Voice"
)

# Launch the app
iface.launch(debug=True)
