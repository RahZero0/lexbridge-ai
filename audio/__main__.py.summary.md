# File: __main__.py

## Purpose
Entry point for the audio package, allowing users to transcribe audio files using Whisper models.

## Key Components
- `argparse` module used to parse command-line arguments.
- `transcribe_file` and `translate_speech_to_english` functions imported from `audio.transcribe` module.
- Command-line options:
  - `--model`: specifies the Whisper model to use (e.g. tiny, base, small).
  - `--language`: forces a specific language for transcription or translation.
  - `--translate`: translates speech to English.

## Important Logic
The script uses a try-except block to catch any import errors and exit with a non-zero status code if an error occurs during transcription or translation. The main function is called when the script is run directly (i.e. not imported as a module).

## Dependencies
- `argparse` module.
- `pathlib` module for working with file paths.

## Notes
This script expects to be run from the parent directory of the `audio` package using the command `python -m audio <file>`.