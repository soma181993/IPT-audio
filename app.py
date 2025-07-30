
from flask import Flask, request, jsonify, render_template, send_from_directory
import gtts
import os
from googletrans import Translator
from datetime import datetime
from langdetect import detect

app = Flask(__name__)

# Serve the main HTML page
@app.route('/')
def home():
    return render_template("main.html")

# Handle translation and audio generation
@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        dest_lang = data.get('dest_lang', 'en')
        src_lang = detect(text)

        translator = Translator()
        translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text

        save_directory = "E:\\IPT\\audio"
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        audio_file_name = f"audio_{current_date}.mp3"
        file_path = os.path.join(save_directory, audio_file_name)

        # Save audio
        tts = gtts.gTTS(translated_text, lang=dest_lang, slow=False)
        tts.save(file_path)

        # Print logs
        print("Incoming JSON:", data)
        print("Translated text:", translated_text)
        print("Audio file saved at:", file_path)

        # Create URL for the frontend
        audio_url = f"/audio/{audio_file_name}"

        return jsonify({
            "translated_text": translated_text,
            "audio_url": audio_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve audio file
@app.route('/audio/<filename>')
def get_audio(filename):
    audio_path = "E:\\IPT\\audio"
    return send_from_directory(audio_path, filename)

if __name__ == '__main__':
    app.run(debug=True)
