import json
import logging
import configparser
from pathlib import Path
from datetime import datetime
import sys
import os

# Import our new modules and existing ones
from logger_setup import setup_logger
from pdf_parser import extract_text_from_pdf
from prayer_selector import parse_prayers, select_prayer_from_cycle
from tts_synthesizer import text_to_speech

def run_daily_prayer_generation():
    """
    Orchestrates the entire process, now driven by logging and configuration.
    """
    # --- Setup Configuration and Logging ---
    # Corrected path logic to be self-contained and robust
    project_root = Path(__file__).resolve().parents[2]
    config = configparser.ConfigParser()
    config.read(project_root / 'config.ini')

    paths = config['Paths']
    tts_config = config['TTS']

    # Initialize the logger
    logger = setup_logger(project_root / paths['LogFile'])
    
    logger.info("Starting the daily prayer generation process...")

    # --- Define File Paths from Config ---
    pdf_path = project_root / paths['PdfFile']
    processed_prayers_path = project_root / paths['ProcessedPrayersFile']
    output_dir = project_root / paths['OutputDir']

    # --- Step 1: Load or Parse Prayers ---
    prayers = []
    if processed_prayers_path.exists():
        logger.info(f"[1/4] Loading prayers from cached file: {paths['ProcessedPrayersFile']}...")
        try:
            with open(processed_prayers_path, 'r', encoding='utf-8') as f:
                prayers = json.load(f)
            # --- ADDED CHECK FOR EMPTY FILE ---
            if not prayers:
                 logger.warning("Cached prayer file is empty. Reparsing from PDF.")
        except json.JSONDecodeError:
            logger.warning("Could not decode JSON from cached file. Reparsing from PDF.")
            prayers = [] # Ensure prayers list is empty to trigger reparsing

    # If prayers list is empty (either because file didn't exist or was invalid), parse the PDF.
    if not prayers:
        logger.info(f"Parsing prayers from PDF: {paths['PdfFile']}...")
        full_text = extract_text_from_pdf(pdf_path)
        if not full_text:
            logger.error("Stopping process: Failed to extract text from PDF.")
            return
        
        prayers = parse_prayers(full_text)
        if prayers:
            processed_prayers_path.parent.mkdir(parents=True, exist_ok=True)
            with open(processed_prayers_path, 'w', encoding='utf-8') as f:
                json.dump(prayers, f, indent=2)
            logger.info(f"Saved {len(prayers)} prayers to cache.")

    if not prayers:
        logger.error("Stopping process: No prayers available.")
        return

    # --- Step 2: Select a Prayer ---
    logger.info("\n[2/4] Selecting a prayer for the day...")
    selected_prayer = select_prayer_from_cycle(prayers)
    if not selected_prayer:
        logger.error("Stopping process: Could not select a prayer.")
        return
    logger.info(f"Selected Prayer: '{selected_prayer['title']}'")

    # --- Step 3: Format the Speech Text ---
    logger.info("\n[3/4] Formatting the text for speech...")
    intro = (
        "...Good morning....... as we pray, please sit in silence for a moment, seeking to be attentive to the presence of God..."
        " the one in whom we live, move and have our being...... "
        "....Father, just as the sun rises in the morning, may our spirits also rise to you this day..."
    )
    prayer_text = f"Today's prayer is titled: {selected_prayer['title']}. \n\n {selected_prayer['body']}..... \n\n All this we ask in the name of Jesus Christ, our Lord and Savior.... AMEN."
    text_for_speech = f"{intro}\n\n{prayer_text}"
    logger.info("Text formatted successfully.")
    
    # --- Step 4: Generate Audio ---
    logger.info("\n[4/4] Generating audio file...")
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"prayer_{today_str}.mp3"
    audio_output_path = output_dir / output_filename
    
    success = text_to_speech(
        text_for_speech, 
        audio_output_path, 
        voice=tts_config['Voice']
        #,        timeout=int(tts_config['Timeout'])
    )

    if success:
        logger.info("\n----------------------------------------------------")
        logger.info("Daily prayer audio generated successfully!")
        logger.info(f"   Find your file at: {audio_output_path}")
        logger.info("----------------------------------------------------")
    else:
        logger.error("\n----------------------------------------------------")
        logger.error("Failed to generate the audio file.")
        logger.error("This could be due to a network timeout or an API issue.")
        logger.error("----------------------------------------------------")

if __name__ == '__main__':
    run_daily_prayer_generation()
