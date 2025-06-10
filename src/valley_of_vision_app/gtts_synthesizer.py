from pathlib import Path
from gtts import gTTS

def text_to_speech(text_to_speak: str, output_filepath: Path) -> bool:
    """
    Converts a string of text into an audio file using the gTTS library.

    Args:
        text_to_speak: The text content to be converted to speech.
        output_filepath: The path where the generated audio file will be saved.

    Returns:
        True if the audio file was created successfully, False otherwise.
    """
    try:
        output_filepath.parent.mkdir(parents=True, exist_ok=True)

        print(f"Generating speech for text... Saving to {output_filepath}")

        tts = gTTS(text=text_to_speak, lang='en', tld='co.uk', slow=False)

        # Save the generated audio to the specified file.
        tts.save(output_filepath)
        
        print("Speech generation successful.")
        return True

    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return False


if __name__ == '__main__':
    # We define a sample prayer for testing purposes.
    sample_prayer = {
        'title': 'A TEST PRAYER',
        'body': 'O Lord, this is a test of the text-to-speech system. '
                'Let this demonstration succeed, that we may glorify thy name '
                'through technology and build a truly inspiring application. Amen.'
    }
    
    # We construct the full text to be spoken.
    full_speech_text = f"{sample_prayer['title']}. {sample_prayer['body']}"

    # Define where to save the output audio file.
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    AUDIO_OUTPUT_PATH = PROJECT_ROOT / "output" / "daily_prayer.mp3"

    # Call our text_to_speech function
    success = text_to_speech(full_speech_text, AUDIO_OUTPUT_PATH)

    if success:
        print(f"\n--- Success! ---")
        print(f"Test audio file created at: {AUDIO_OUTPUT_PATH}")
        print("Please play the file to verify the audio.")
        print("------------------")
    else:
        print("\n--- Failed to create audio file. ---")
