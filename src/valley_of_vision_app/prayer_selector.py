import re
import json
import random
import configparser
from pathlib import Path
from typing import List, Dict, Optional

# --- ADDED BACK THE MISSING FUNCTION ---
def parse_prayers(full_text: str) -> List[Dict]:
    """
    Parses the full text of the book to extract individual prayers.

    This function looks for prayer titles (which are typically in all-caps)
    to identify the start of each prayer.

    Args:
        full_text: A string containing the entire text of the PDF.

    Returns:
        A list of dictionaries, where each dictionary represents a prayer
        and has 'title' and 'body' keys.
    """
    # This regular expression finds titles (all-caps phrases between newlines).
    pattern = re.compile(r"\n\n([A-Z'’\s]{5,})\n", re.MULTILINE)

    # We use re.split() to break the text apart wherever a title is found.
    parts = pattern.split(full_text)

    prayers = []
    # We start at index 1 (skipping intro text) and jump by 2 each time.
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        if i + 1 < len(parts):
            body = parts[i+1].strip()
            prayers.append({'title': title, 'body': body})

    return prayers
# --- END OF ADDED FUNCTION ---


def _get_prayer_log_path(project_root: Path) -> Path:
    """Helper function to define the path for our prayer log."""
    # Corrected path to find config.ini in the project root
    config_path = project_root / 'config.ini'
    if config_path.exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        return project_root / config['Paths']['PrayerLogFile']
    # Fallback to default if config file is not found
    return project_root / "data" / "processed" / "prayer_log.json"

def _load_used_prayers(log_path: Path) -> List[str]:
    """Loads the list of used prayer titles from the log file."""
    if not log_path.exists():
        return []
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return [] # Return empty list if log file is corrupted or empty

def _save_used_prayers(log_path: Path, used_titles: List[str]):
    """Saves the list of used prayer titles to the log file."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(used_titles, f, indent=2)

def select_prayer_from_cycle(all_prayers: List[Dict]) -> Optional[Dict]:
    """
    Selects a prayer, ensuring no repeats until all prayers have been used once.
    """
    if not all_prayers:
        return None

    # Define paths and load the log of used prayer titles
    project_root = Path(__file__).resolve().parents[2]
    log_path = _get_prayer_log_path(project_root)
    used_titles = _load_used_prayers(log_path)

    all_titles = [p['title'] for p in all_prayers]
    available_titles = [title for title in all_titles if title not in used_titles]

    if not available_titles:
        print("Cycle complete. Resetting the prayer list and starting anew.")
        used_titles = []
        available_titles = all_titles
    
    selected_title = random.choice(available_titles)
    used_titles.append(selected_title)
    _save_used_prayers(log_path, used_titles)

    for prayer in all_prayers:
        if prayer['title'] == selected_title:
            return prayer

    return None
