# File: chunk.py

## Purpose
Chunked transcription pipeline for multilingual audio files. It splits the audio into smaller chunks based on silence, detects the language of each chunk, and transcribes it with explicit language. The resulting transcripts are then merged to form a single output.

## Key Components

*   `detect_nonsilent()`: Finds non-silent regions in the audio.
*   `_ms_label()`: Converts milliseconds to a formatted time string (e.g., "00:01:02").
*   `transcribe_chunked()`: The main function that implements the chunked transcription pipeline.

## Important Logic

1.  Load audio with pydub and split it into chunks based on silence using `detect_nonsilent()`.
2.  For each chunk, detect the language using `model.detect_language()` and transcribe it with explicit language using `model.transcribe()`.
3.  Merge the transcripts from all chunks to form a single output.

## Dependencies

*   pydub
*   whisper
*   torch (optional)

## Notes

*   This pipeline is designed for multilingual audio files and can handle mixed-language audio.
*   It uses explicit language transcription, which provides more accurate results than one-shot Whisper on mixed-language audio.