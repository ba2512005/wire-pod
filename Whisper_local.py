import os
import traceback
import time
import asyncio

import numpy as np
from flask import Flask, jsonify, request
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

app = Flask(__name__)

# Load your model and setup preprocessing here
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = os.getenv("sttModel", "openai/whisper-tiny.en")

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

# Define a route to process audio
@app.route('/process-audio', methods=['POST'])
async def process_audio():
    response_q = asyncio.Queue()
    try:
        start_time = time.time()
        # Access the audio data from the POST request
        audio_data = request.files['file'].read()  # Read the audio file data directly
        audio_array = np.frombuffer(audio_data, dtype=np.int16)  # Create the audio array
        result = pipe(audio_array)
        time.sleep(1) # Process the audio using your model pipeline (`pipe`)
        end_time = time.time()
        print(f"Processing time: {end_time - start_time} seconds")
        # Extract the transcribed text from the result
        text_result = result["text"]

        # Return the processed text as a JSON response
        return jsonify({'Text': text_result, 'elapsed_time': end_time - start_time})

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(e)}"
        error_info = traceback.format_exc()
        traceback.print_exc()
        return jsonify({'error': error_message, 'traceback': error_info}), 500  # HTTP status code 500 for internal server error

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app