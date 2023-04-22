#!/usr/bin/env python3
"""
Generate captions for a video using OpenAI's Whisper API
"""

import argparse
import openai
import sys
import os
import mimetypes
import tempfile

from pathlib import Path
from pydub import AudioSegment

TWENTYFIVE_MB = 26214400
TEMP_DIR = Path(tempfile.gettempdir())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", help="Path to media file", type=Path)
    parser.add_argument("output", help="Path to output file", type=Path)
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (default: read from OPENAI_API_KEY environment variable)",
        default=os.environ.get("OPENAI_API_KEY"),
    )
    parser.add_argument(
        "--prompt",
        help="Prompt to use as a context to the model "
        + "(e.g. The media's summary or script). Can be a file path or a string.",
        default="",
    )
    parser.add_argument(
        "--output-format",
        help="Output format (default: srt, can also be vtt)",
        default="srt",
    )
    parser.add_argument(
        "--language",
        help="Language of the input media for transcribing"
        + " (default: en, must be in ISO 639-1 format and supported by OpenAI's Whisper API)."
        + " For translating, the language is automatically detected"
        + " and the output language is always English.",
    )
    parser.add_argument(
        "--translate-to-english",
        help="Translate the input media to English before generating captions",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    return generate_captions(
        args.media,
        args.output,
        args.api_key,
        args.prompt,
        args.output_format,
        args.language,
        args.translate_to_english,
    )


def generate_captions(
    media: Path,
    output: Path,
    api_key: str = os.environ.get("OPENAI_API_KEY"),
    prompt: str = "",
    format: str = "srt",
    language: str = "en",
    translate: bool = False,
):
    if not media.is_file():
        print(f"Media file {media} does not exist")
        return 1

    if not api_key:
        print("OpenAI API key is required, none provided or found in environment")
        return 1

    supported_formats = ["srt", "vtt"]
    if format not in supported_formats:
        print(
            f"Output format {format} is not supported. Must be one of: {supported_formats}"
        )
        return 1

    transcribe = openai.Audio.translate if translate else openai.Audio.transcribe
    transcribe_or_translate = "Translating" if translate else "Transcribing"
    language = "en" if translate else language

    try:
        if Path(prompt).is_file():
            with open(prompt, "r") as f:
                prompt = f.read()
    except Exception:
        # Let's suppress any errors here (e.g. due to large filename size)
        # and just use the prompt as a string
        pass

    audio = get_audio(media)
    audio_size = audio.stat().st_size
    if audio_size > TWENTYFIVE_MB:
        print(
            f"Audio file is too large {audio_size / 1000000}MB, must be less than 25MB, attempting to downsample"
        )
        audio = downsample_audio(audio, TWENTYFIVE_MB)
        audio_size = audio.stat().st_size
    print(f"Audio file size in MB: {audio_size / 1000000}")

    openai.api_key = api_key
    print(f"{transcribe_or_translate} using OpenAI's Whisper AI to {format} format")
    with open(audio, "rb") as f:
        transcript = transcribe(
            "whisper-1", f, response_format=format, language=language, prompt=prompt
        )
    print(f"Transcription complete, saving to {output}")
    with open(output, "w") as f:
        f.write(transcript)

    return 0


def get_audio(media: Path):
    print(f"Getting audio from {media}")
    type = mimetypes.guess_type(media)[0]
    if type == "audio":
        print("Media is already audio, no need to convert")
        return media

    audio = TEMP_DIR / "audio.mp3"
    AudioSegment.from_file(media).set_channels(1).export(
        audio, format="mp3", bitrate="128k"
    )
    print(f"Split audio file and saved to {audio}")
    return audio


def downsample_audio(audio: Path, max_size: int = TWENTYFIVE_MB):
    print(f"Downsampling audio from {audio}")
    bitrates = ["64k", "32k", "16k"]
    for bitrate in bitrates:
        downsampled = TEMP_DIR / "audio_downsampled.mp3"
        AudioSegment.from_file(audio).set_channels(1).export(
            downsampled, format="mp3", bitrate=bitrate
        )
        if downsampled.stat().st_size < max_size:
            print(
                f"Downsampled audio file and saved to {downsampled} with bitrate {bitrate}"
            )
            return downsampled

    print("Unable to downsample audio file, it needs to be split into smaller chunks")
    print("Open a feature request on GitHub if you need this feature")
    raise Exception("Unable to downsample audio file")


if __name__ == "__main__":
    sys.exit(main())
