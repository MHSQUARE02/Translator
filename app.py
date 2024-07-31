from flask import Flask, request, jsonify, render_template
from googletrans import Translator
import speech_recognition as sr
import os
import logging
import tempfile
import subprocess
from gtts import gTTS
from io import BytesIO
import base64

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define language code mapping
language_name_to_code = {
    'afrikaans': 'af', 'albanian': 'sq', 'arabic': 'ar', 'armenian': 'hy',
    'bengali': 'bn', 'bosnian': 'bs', 'catalan': 'ca', 'croatian': 'hr',
    'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en',
    'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi',
    'french': 'fr', 'german': 'de', 'greek': 'el', 'gujarati': 'gu',
    'hindi': 'hi', 'hungarian': 'hu', 'icelandic': 'is', 'indonesian': 'id',
    'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn',
    'khmer': 'km', 'korean': 'ko', 'latin': 'la', 'latvian': 'lv',
    'lithuanian': 'lt', 'macedonian': 'mk', 'malayalam': 'ml', 'marathi': 'mr',
    'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'polish': 'pl',
    'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru',
    'serbian': 'sr', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl',
    'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv',
    'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr',
    'ukrainian': 'uk', 'urdu': 'ur', 'vietnamese': 'vi', 'welsh': 'cy',
    'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    temp_audio_path = None
    converted_audio_path = None
    
    try:
        audio = request.files['file']

        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_audio_file:
            audio.save(temp_audio_file.name)
            temp_audio_path = temp_audio_file.name

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
            converted_audio_path = temp_wav_file.name

        # Convert the audio file to a format that speech_recognition can process
        conversion_command = [
            'ffmpeg', '-i', temp_audio_path, '-ac', '1', '-ar', '16000', '-y', converted_audio_path
        ]
        subprocess.run(conversion_command, check=True)

        recognizer = sr.Recognizer()
        with sr.AudioFile(converted_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        return jsonify({'transcription': text})

    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        return jsonify({'error': 'Speech recognition request failed.'}), 500
    except sr.UnknownValueError:
        logging.error("Google Speech Recognition could not understand audio")
        return jsonify({'error': 'Speech recognition could not understand audio.'}), 400
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if converted_audio_path and os.path.exists(converted_audio_path):
            os.remove(converted_audio_path)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.form['text']
        target_language = request.form['language']
        translator = Translator()
        translated_text = translator.translate(text, dest=target_language).text
        
        # Convert translated text to audio
        tts = gTTS(text=translated_text, lang=target_language)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_data = audio_fp.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        return jsonify({'translated_text': translated_text, 'audio': audio_base64})
    except Exception as e:
        logging.error(f"An error occurred during translation: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error starting the Flask application: {e}")
