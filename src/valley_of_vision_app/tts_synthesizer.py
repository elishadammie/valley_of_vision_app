import os
import httpx
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

def text_to_speech(text_to_speak: str, output_filepath: Path, voice: str = "onyx") -> bool:
    """
    Converts a string of text into an audio file using OpenAI's standard TTS API.

    Args:
        text_to_speak: The text content to be converted to speech.
        output_filepath: The path where the generated audio file will be saved.
        voice: The desired voice model from OpenAI. 'onyx' is a deep, professional voice.

    Returns:
        True if the audio file was created successfully, False otherwise.
    """
    try:
        # Explicitly find and load the .env file from the project root.
        project_root = Path(__file__).resolve().parents[2]
        dotenv_path = project_root / '.env'
        
        if not dotenv_path.is_file():
            print(f"Error: .env file not found at {dotenv_path}")
            return False

        load_dotenv(dotenv_path=dotenv_path)

        # Retrieve the API key from environment variables.
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            print("Error: OPENAI_API_KEY was not found in your .env file.")
            return False
        
        # --- MODIFICATION FOR SSL ERROR ---
        # Create a custom httpx client that disables SSL certificate verification.
        http_client = httpx.Client(verify=False)
        
        # Initialize the OpenAI client. It will use the standard API endpoint but with our custom client.
        client = OpenAI(api_key=api_key, http_client=http_client)
        # --- END MODIFICATION ---

        output_filepath.parent.mkdir(parents=True, exist_ok=True)

        print(f"Generating speech with OpenAI voice '{voice}'... Saving to {output_filepath}")

        # Make the API call to the TTS endpoint.
        response = client.audio.speech.create(
            model="tts-1-hd",  # Using the high-definition model for best quality
            voice=voice,
            input=text_to_speak
        )

        # Stream the audio content directly to the specified file.
        response.stream_to_file(output_filepath)
        
        print("Speech generation successful.")
        return True

    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return False


if __name__ == '__main__':
    # Test script to verify functionality
    test_text = "This is a test of the official OpenAI text-to-speech service using the onyx voice."
    
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    AUDIO_OUTPUT_PATH = PROJECT_ROOT / "output" / "daily_prayer_openai_final.mp3"

    success = text_to_speech(test_text, AUDIO_OUTPUT_PATH)

    if success:
        print(f"\n--- Success! ---")
        print(f"Test audio file created at: {AUDIO_OUTPUT_PATH}")
        print("Please play the file to verify the premium audio quality.")
        print("------------------")
    else:
        print("\n--- Failed to create audio file. Check your API key and network connection. ---")
