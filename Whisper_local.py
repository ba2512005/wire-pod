import os
import traceback
import time
import asyncio
import ffmpeg
import numpy as np
import whisper
from flask import Flask, jsonify, request
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

app = Flask(__name__)

# Load your model and setup preprocessing here
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = os.getenv("sttModel", "openai/whisper-medium")

model = whisper.load_model(model_id, device=device, dtype=torch_dtype)
# Define a route to process audio
@app.route('/process-audio', methods=['POST'])
async def process_audio():
    response_q = asyncio.Queue()
    try:
        file = request.files['file']
        start_time = time.time()
        # Access the audio data from the POST request
        if isinstance(file, bytes):
            inp = file
            file = 'pipe:'
        else:
            inp = None

        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input(file, threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=inp)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        audio_array = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

        #audio_data = request.files['file'].read()  # Read the audio file data directly
        #audio_array = np.frombuffer(audio_data, dtype=np.int16)  # Create the audio array
        result = pipe(audio_array)
        time.sleep(1) # Process the audio using your model pipeline (`pipe`)
        end_time = time.time()
        print(f"Processing time: {end_time - start_time} seconds")
        # Extract the transcribed text from the result
        text_result = result["text"]

        # Return the processed text as a JSON response
        return jsonify({'Text': text_result})

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(e)}"
        error_info = traceback.format_exc()
        traceback.print_exc()
        return jsonify({'error': error_message, 'traceback': error_info}), 500  # HTTP status code 500 for internal server error

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app