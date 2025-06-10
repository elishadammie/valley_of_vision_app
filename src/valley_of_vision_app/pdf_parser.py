# We use the 'pathlib' library for handling file paths. It's a modern,
# object-oriented way to work with the filesystem that works across
# Windows, macOS, and Linux without issues.
from pathlib import Path

# We import the 'fitz' library, which is the core of PyMuPDF.
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extracts all text content from a given PDF file.

    Args:
        pdf_path: A Path object pointing to the PDF file.

    Returns:
        A single string containing all the extracted text from the PDF.
        Returns an empty string if the file is not found or is not a valid PDF.
    """
    # First, we check if the provided path actually exists and is a file.
    # This is a good practice to prevent errors.
    if not pdf_path.is_file():
        print(f"Error: File not found at {pdf_path}")
        return ""

    try:
        # We open the PDF file using fitz.open(). The 'with' statement ensures
        # that the file is properly closed even if errors occur.
        with fitz.open(pdf_path) as doc:
            full_text = []
            # We loop through each page in the document.
            for page in doc:
                # For each page, we extract the text using page.getText().
                # The text is then appended to our list.
                full_text.append(page.get_text())
            
            # Finally, we join all the text pieces from each page into one
            # single string, with each page's content separated by a newline.
            return "\n".join(full_text)
    except Exception as e:
        # If any error occurs during the process (e.g., the file is corrupt),
        # we catch the exception, print an error message, and return an empty string.
        print(f"An error occurred while processing the PDF: {e}")
        return ""

# The __name__ == "__main__" block is a standard Python convention.
# The code inside this block will only run when you execute this script directly
# (e.g., by running `python src/valley_of_vision_app/pdf_parser.py` in the terminal).
# It will NOT run if this file is imported as a module into another script.
# This makes our code reusable and testable.
if __name__ == "__main__":
    # We construct the path to the PDF file.
    # Path(__file__) gives the path to the current script (pdf_parser.py).
    # .resolve() makes it an absolute path.
    # .parents[2] goes up two directories (from src/valley_of_vision_app to the project root).
    # Then we join it with the path to our PDF.
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    PDF_FILE_PATH = PROJECT_ROOT / "data" / "raw" / "The Valley of Vision.pdf"

    print(f"Attempting to extract text from: {PDF_FILE_PATH}")
    
    extracted_text = extract_text_from_pdf(PDF_FILE_PATH)

    if extracted_text:
        print("\n--- Successfully extracted text! ---")
        # We print only the first 500 characters as a preview.
        print("Preview of extracted text:")
        print(extracted_text[:500])
        print("\n------------------------------------")
    else:
        print("\n--- Failed to extract text. Please check the file path and ensure it's a valid PDF. ---")
