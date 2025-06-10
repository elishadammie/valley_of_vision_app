from pathlib import Path
from datetime import datetime

# Import the functions from our other modules.
# The '.' before the module name indicates it's a relative import
# from within the same package (the valley_of_vision_app directory).
from pdf_parser import extract_text_from_pdf
from prayer_selector import parse_prayers, select_random_prayer
from tts_synthesizer import text_to_speech

def run_daily_prayer_generation():
    """
    Orchestrates the entire process of generating the daily prayer audio file.
    """
    print("Starting the daily prayer generation process...")

    # --- Define File Paths ---
    # We establish all our paths relative to this file's location.
    # This makes the script portable and reliable.
    current_dir = Path(__file__).parent
    project_root = current_dir.parents[1]
    pdf_path = project_root / "data" / "raw" / "The Valley of Vision.pdf"
    output_dir = project_root / "output"

    # --- Step 1: Extract Text from PDF ---
    print(f"\n[1/4] Extracting text from {pdf_path.name}...")
    full_text = extract_text_from_pdf(pdf_path)
    if not full_text:
        print("Stopping process: Failed to extract text from PDF.")
        return

    # --- Step 2: Parse Prayers ---
    print("[2/4] Parsing individual prayers from the text...")
    prayers = parse_prayers(full_text)
    if not prayers:
        print("Stopping process: Failed to parse prayers.")
        return
    print(f"Successfully parsed {len(prayers)} prayers.")

    # --- Step 3: Select a Prayer ---
    print("[3/4] Selecting a random prayer for the day...")
    selected_prayer = select_random_prayer(prayers)
    if not selected_prayer:
        print("Stopping process: Could not select a prayer.")
        return
    print(f"Selected Prayer: '{selected_prayer['title']}'")

    # --- Step 4: Generate Audio ---
    # We'll create a unique filename for each day's prayer.
    # e.g., "prayer_2024-12-25.mp3"
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"prayer_{today_str}.mp3"
    audio_output_path = output_dir / output_filename
    
    # Format the text to be spoken, including a title announcement.
    text_for_speech = f"Today's prayer is titled: {selected_prayer['title']}. \n\n {selected_prayer['body']}"
    
    print(f"[4/4] Generating audio file at {audio_output_path}...")
    success = text_to_speech(text_for_speech, audio_output_path)

    if success:
        print("\n----------------------------------------------------")
        print("✅ Daily prayer audio generated successfully!")
        print(f"   Find your file at: {audio_output_path}")
        print("----------------------------------------------------")
    else:
        print("\n----------------------------------------------------")
        print("❌ Failed to generate the audio file.")
        print("----------------------------------------------------")


if __name__ == '__main__':
    # When we run `python main.py`, this block gets executed.
    run_daily_prayer_generation()

