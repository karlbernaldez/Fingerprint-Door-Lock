import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# # Set up the ElevenLabs client
# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# if not ELEVENLABS_API_KEY:
#     raise ValueError("ELEVENLABS_API_KEY environment variable not set")
client = ElevenLabs(api_key="sk_6f71b4a9f299dd73de333e14e7289bc4930886700727717b")

def text_to_speech_file(text: str) -> str:
    try:
        # Calling the text_to_speech conversion API with detailed parameters
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",  # Use the turbo model for low latency
            voice_settings=VoiceSettings(
                stability=1.0,
                similarity_boost=1.0,
                style=1.0,
                use_speaker_boost=True,
            ),
        )

        # Ensure the directory exists
        save_file_path = "../sounds/welcome.mp3"
        os.makedirs(os.path.dirname(save_file_path), exist_ok=True)

        # Writing the audio to a file
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"{save_file_path}: A new audio file was saved successfully!")

        # Return the path of the saved audio file
        return save_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
