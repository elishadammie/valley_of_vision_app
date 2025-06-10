import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def text_to_speech(text_to_speak: str, output_filepath: Path, voice_id: str = "00001") -> bool:
    """
    Converts text to speech by sending a direct request to the ttsopenai.com API.

    Args:
        text_to_speak: The text content to be converted to speech.
        output_filepath: The path where the generated audio file will be saved.
        voice_id: The specific voice ID to use from the ttsopenai.com service.

    Returns:
        True if the audio file was created successfully, False otherwise.
    """
    try:
        # --- Load Environment Variables ---
        project_root = Path(__file__).resolve().parents[2]
        dotenv_path = project_root / '.env'
        
        if not dotenv_path.is_file():
            print(f"Error: .env file not found at {dotenv_path}")
            return False

        load_dotenv(dotenv_path=dotenv_path)

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            print("Error: OPENAI_API_KEY was not found in your .env file.")
            return False

        # --- Construct the API Request ---
        # This URL is taken directly from the API documentation you found.
        url = "https://api.ttsopenai.com/uapi/v1/text-to-speech"

        # The headers must match what the service expects.
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }

        # The data payload must also match the service's requirements.
        data = {
            "model": "tts-1",
            "voice_id": voice_id,
            "speed": 1,
            "input": text_to_speak
        }

        output_filepath.parent.mkdir(parents=True, exist_ok=True)
        print(f"Generating speech via {url}... Saving to {output_filepath}")

        # --- Make the POST request ---
        # We set a timeout and disable SSL verification as a precaution.
        response = requests.post(url, headers=headers, json=data, timeout=60, verify=False)

        # Check if the request was successful. A status code of 200 means OK.
        if response.status_code == 200:
            # The audio data is in the response's content. We write it to a file.
            with open(output_filepath, 'wb') as f:
                f.write(response.content)
            print("Speech generation successful.")
            return True
        else:
            # If the status is not 200, print the error details from the server.
            print(f"An error occurred. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return False


if __name__ == '__main__':
    sample_prayer = {
        'title': 'A TEST PRAYER WITH MANUAL API',
        'body': 'O Lord, this is a test using a manual request. Let this succeed.'
    }
    
    full_speech_text = f"{sample_prayer['title']}. \n\n {sample_prayer['body']}"
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    AUDIO_OUTPUT_PATH = PROJECT_ROOT / "output" / "daily_prayer_manual_api.mp3"

    # We can test different voice_id's here if needed.
    success = text_to_speech(full_speech_text, AUDIO_OUTPUT_PATH, voice_id="00001")

    if success:
        print(f"\n--- Success! ---")
        print(f"Test audio file created at: {AUDIO_OUTPUT_PATH}")
        print("Please play the file to verify the audio.")
        print("------------------")
    else:
        print("\n--- Failed to create audio file. Please check your .env file and network connection. ---")
