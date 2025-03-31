from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import google.generativeai as genai
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Set up Gemini API key
genai.configure(api_key="")

def generate_story_text(prompt):
    """Generates a story using Gemini AI."""
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

def convert_text_to_speech(text):
    """Converts the given text to speech and saves it as an audio file."""
    tts = gTTS(text=text, lang='en')
    audio_path = "static/story.mp3"
    tts.save(audio_path)
    return audio_path

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/generate_story', methods=['POST'])
def generate_story():
    """API endpoint to generate a story and convert it to speech."""
    data = request.json
    prompt = data.get("prompt", "Once upon a time...")
    
    story = generate_story_text(prompt)
    audio_path = convert_text_to_speech(story)
    
    return jsonify({"story": story, "audio_url": audio_path})

if __name__ == '__main__':
    app.run(debug=True)
