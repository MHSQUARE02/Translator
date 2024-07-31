# Translator
""Hack4change Challenge""
**DISCLAIMER-** https://mhsquare02.github.io/Translator/ 
    This is just our static web application deployed using github repository. We have attached our github repository link and also explained detailly how to run and launch our web application locally below,
    
Translator/
│
├── templates/
│   └── index.html           # HTML file for the web interface
│
├── app.py                   # Main Flask application
├── requirements.txt         # List of Python dependencies
├── README.md                # Project README file


Translator with Speech Recognition and Translation
This project is a web application that enables users to upload audio files, transcribe them into text, and translate the transcriptions into different languages. The application uses Flask for the backend, Google Speech Recognition for transcription, Google Translate for translation, and gTTS for converting text to speech.

Features
Upload audio files in .webm format for transcription.
Transcribe audio to text using Google Speech Recognition.
Translate transcribed text to various languages supported by Google Translate.
Convert translated text to speech and download as an audio file.
Simple and intuitive web interface.
Technologies Used
Flask: A micro web framework for Python.
Google Speech Recognition: For transcribing audio files to text.
Google Translate: For translating text to different languages.
gTTS (Google Text-to-Speech): For converting translated text to speech.
HTML/CSS/JavaScript: For the frontend.
Installation
Clone the repository

bash
Copy code
git clone https://mhsquare02.github.io/Translator/ 
cd tamil-translator
Create and activate a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows use venv\Scripts\activate
Install the dependencies

bash
Copy code
pip install -r requirements.txt
Run the application

bash
Copy code
python app.py
Access the application
Open your web browser and go to http://127.0.0.1:5000.

Usage
Upload an Audio File

Navigate to the home page.
Click on the "Choose File" button to select your audio file (.webm format).
Click on the "Upload" button to upload and transcribe the audio file.
Transcription

The transcribed text will be displayed on the page.
Translation

Select the target language from the dropdown menu.
Click on the "Translate" button to translate the text.
The translated text will be displayed on the page.
Text-to-Speech

The translated text will be converted to speech and available for download as an audio file.
Contributing
Contributions are welcome! Please create an issue or pull request for any feature requests, bug fixes, or enhancements.

