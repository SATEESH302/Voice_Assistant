from flask import Flask, request, jsonify, render_template
import os
import wave
import numpy as np
from scipy.io import wavfile
from io import BytesIO
from sppech_to_text import get_answer_for_question

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("sound.html")


@app.route("/api/process_audio", methods=["POST"])
def process_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    # Save the audio file
    audio_file.save("output.wav")

    # Process the audio file
    text = get_answer_for_question("output.wav")

    return jsonify({"text": text})


if __name__ == "__main__":
    app.run(debug=True)
