# File: transcribe.py

## Purpose
Transcribes audio files using the Whisper speech recognition model, providing text and detected language results.

## Key Components
* `transcribe_file` function: Transcribes an audio file and returns a `TranscriptionResult` object with text and language information.
* `translate_speech_to_english` function: Translates spoken content to English and returns a `SpeechToEnglishResult` object with translated text and source language information.
* Whisper model caching using `_model_cache` dictionary.

## Important Logic
* Model sizes can be set to different Whisper models (e.g., "base", "small", "medium", etc.) for varying levels of accuracy and speed.
* Language detection is handled by Whisper's built-in tokenizer, which maps language codes to full names.
* The `clear_model_cache` function clears loaded Whisper models to free up VRAM/RAM.

## Dependencies
* `whisper` library: Requires the openai-whisper package installed via pip.
* `ffmpeg` executable: Installed and accessible on the system's PATH.

## Notes
* This script assumes that ffmpeg is installed and accessible. If not, it will raise an ImportError.
* The `_ensure_ffmpeg_on_path` function prepends /opt/homebrew/bin to PATH for ffmpeg if necessary.
* Whisper model sizes can be adjusted to balance quality and speed for specific use cases.