# The 're' module is Python's standard library for working with regular expressions.
# We'll use it to find the prayer titles in our text.
import re
# The 'random' module will allow us to pick a prayer at random.
import random
from pathlib import Path

# We are importing the function we created in our previous step.
# This is a key principle of modular software design: reusing code.
from pdf_parser import extract_text_from_pdf

def parse_prayers(full_text: str) -> list[dict]:
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
    # This regular expression is the key to our parser.
    pattern = re.compile(r"\n\n([A-Z'’\s]{5,})\n", re.MULTILINE)

    # We use re.split() to break the text apart wherever our pattern (a title) is found.
    # The result is a list where titles and prayer bodies alternate.
    # Example: ['intro text', 'TITLE 1', 'prayer body 1', 'TITLE 2', 'prayer body 2', ...]
    parts = pattern.split(full_text)

    # The first part is the book's introductory text before the first prayer, so we skip it.
    # We step through the list two items at a time: one for the title, one for the body.
    prayers = []
    # We start at index 1 and jump by 2 each time.
    for i in range(1, len(parts), 2):
        # The title is the first item in our pair. .strip() removes leading/trailing whitespace.
        title = parts[i].strip()
        # The prayer body is the second item.
        # We need to check if there is a next part to avoid an IndexError.
        if i + 1 < len(parts):
            body = parts[i+1].strip()
            prayers.append({'title': title, 'body': body})

    return prayers

def select_random_prayer(prayers: list[dict]) -> dict | None:
    """
    Selects a single prayer at random from a list of prayers.

    Args:
        prayers: A list of prayer dictionaries.

    Returns:
        A single prayer dictionary, or None if the list is empty.
    """
    if not prayers:
        return None
    return random.choice(prayers)


# This block will run only when the script is executed directly.
if __name__ == '__main__':
    # We use the same method as before to locate our project root and PDF file.
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    PDF_FILE_PATH = PROJECT_ROOT / "data" / "raw" / "The Valley of Vision.pdf"

    print("Step 1: Extracting text from PDF...")
    full_text = extract_text_from_pdf(PDF_FILE_PATH)

    if full_text:
        print("Step 2: Parsing prayers from extracted text...")
        prayers_list = parse_prayers(full_text)

        if prayers_list:
            print(f"\n--- Success! Found {len(prayers_list)} prayers. ---")

            print("\nStep 3: Selecting a random prayer...")
            selected_prayer = select_random_prayer(prayers_list)

            if selected_prayer:
                print("\n--- Random Prayer ---")
                print(f"Title: {selected_prayer['title']}")
                print(f"Body Preview: {selected_prayer['body'][:150]}...")
                print("----------------------")
            else:
                print("Could not select a random prayer.")
        else:
            print("\n--- Failed to parse any prayers from the text. ---")
    else:
        print("\n--- Could not extract text from PDF to parse. ---")

