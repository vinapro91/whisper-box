# Whisper Transcription API

This project provides a simple REST API using Flask to transcribe audio files (mp3, wav, etc) using OpenAI's Whisper (base model).

## Features

- POST `/transcribe` endpoint
- Accepts audio files via `multipart/form-data` (field name: `file`)
- Returns transcription as JSON: `{ "transcription": "..." }`
- Handles errors for invalid audio or transcription failures
- Temporary file handling for processing

## Requirements

- Python 3.10+
- ffmpeg (for audio processing)

## Running Locally (without Docker)

1. Install ffmpeg:
   ```sh
   sudo apt update && sudo apt install ffmpeg
   ```
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the API:
   ```sh
   python app.py
   ```
4. The API will be available at `http://localhost:5000/transcribe`

## Running with Docker

1. Build the Docker image:
   ```sh
   docker build -t whisper-api .
   ```
2. Run the container:
   ```sh
   docker run -p 5000:5000 whisper-api
   ```
3. The API will be available at `http://localhost:5000/transcribe`

## Usage Example

Send a POST request with an audio file:

```sh
curl -X POST http://localhost:5000/transcribe \
  -F "file=@/path/to/your/audio.mp3"
```

Response:

```json
{
  "transcription": "your transcribed text here"
}
```

## Notes

- Only the Whisper "base" model is used for transcription.
- Temporary files are deleted after processing.
- Error messages are returned in JSON format.
