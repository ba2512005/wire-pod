import os
import traceback

from flask import Flask, jsonify, request
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

app = Flask(__name__)

# Load your model and setup preprocessing here
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = os.getenv("sttModel", "openai/whisper-medium")

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
def process_audio():
    try:
        # Access the audio data from the POST request
        audio_file = request.files['file']
        file = "audio.mp3"

        # Save the received audio to a file
        audio_file.save(file)

        # Process the audio using your model pipeline (`pipe`)
        result = pipe(audio_file)
        text_result = result["text"]

        # Return the processed text as a JSON response
        return jsonify({'transcribed_text': text_result})

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(e)}"
        error_info = traceback.format_exc()
        traceback.print_exc()
        return jsonify({'error': error_message, 'traceback': error_info}), 500  # HTTP status code 500 for internal server error

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app