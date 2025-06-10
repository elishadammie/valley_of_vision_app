# Valley of Vision - Daily Prayer App

![Project Banner](https://www.centraloaks.com/wp-content/uploads/2018/05/valley-of-vision-image-2.jpg)

A personal application designed to bring a moment of peace and reflection to your evening. This script extracts a prayer from the Puritan collection "The Valley of Vision," converts it to a soothing audio file using Text-to-Speech (TTS) technology, and delivers it daily.

## ✨ Features

* **PDF Text Extraction:** Parses prayers directly from the "Valley of Vision" PDF.
* **High-Quality TTS:** Converts prayer text into a deep, masculine, and soothing voice.
* **Automated Scheduling:** Designed to be run automatically at a set time each day.
* **Personal Delivery:** Sends the generated audio file for personal evening reflection.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.8+
* `pip` and `venv` (usually included with Python)
* The `valley_of_vision.pdf` file placed in the `data/raw/` directory.

### Installation

1.  **Clone the repository (if you are using Git):**
    ```sh
    git clone [https://github.com/your_username/valley_of_vision_app.git](https://github.com/your_username/valley_of_vision_app.git)
    cd valley_of_vision_app
    ```

2.  **Create and activate a virtual environment:**
    * **On macOS/Linux:**
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows:**
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    *(We will create this file in our next step)*
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Copy the example file to a new `.env` file. This file will hold your secret keys and configurations.
    ```sh
    cp .env.example .env
    ```
    Then, open the `.env` file and add the necessary values.

## Usage

To run the script manually and generate a prayer for the day, execute the main script:

```sh
python src/valley_of_vision_app/main.py
```

## ⚙️ Configuration

The application requires the following environment variables to be set in your `.env` file:

| Variable        | Description                                       | Example                       |
| --------------- | ------------------------------------------------- | ----------------------------- |
| `TTS_API_KEY`   | The API key for your chosen Text-to-Speech service. | `sk-xxxxxxxxxxxxxxxxxxxxxxx`  |
| `DELIVERY_CONFIG` | Configuration details for the delivery mechanism. | `(Details to be added later)` |

## acknowledgments

* Based on the book of prayers, "The Valley of Vision: A Collection of Puritan Prayers & Devotions."

## 📄 License

This project is for personal use. If you choose to share it, consider a license like the [MIT License](https://choosealicense.com/licenses/mit/).

