#!/usr/bin/env python3
"""
Generate captions for a video using OpenAI's Whisper API
"""

import argparse
import sys
import os
import mimetypes
import tempfile

from pathlib import Path
from pydub import AudioSegment

import openai
import pysrt

TWENTYFIVE_MB = 26214400
TEMP_DIR = Path(tempfile.gettempdir())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", help="Path to media file", type=Path)
    parser.add_argument(
        "--output",
        help="Path to output file (default: The same filename as the input media file in the same directory)",
        type=Path,
        default=None,
    )
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
        choices=["srt", "vtt"],
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
    parser.add_argument(
        "--run-whisper-locally",
        help="Use the local Whisper model instead of the OpenAI API. Does not require an API key.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--highlight-words",
        help="Highlight each word in the captions as they are spoken. Will run Whisper locally.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--highlight-color",
        choices=["bold", "red", "green", "blue", "yellow", "magenta", "cyan", "white"],
        help="Color of the highlight. Will run Whisper locally and highlight words.",
        default=None,
    )
    parser.add_argument(
        "--max-words-per-caption",
        help="Maximum number of words per caption, if none provided, will be automatically determined."
        + " Will run Whisper locally.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--captions-font",
        help="Font used for the captions. It must be installed on your system.",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--captions-font-size",
        help="Font size (in px) used for the captions.",
        type=int,
        default=None,
    )
    args = parser.parse_args()

    local_whisper_options = {
        "highlight_words": args.highlight_words,
        "highlight_color": args.highlight_color,
        "max_words_per_caption": args.max_words_per_caption,
    }

    font_options = {
        "font": args.captions_font,
        "font_size": args.captions_font_size,
    }

    exit_code, exit_message = generate_captions(
        media=args.media,
        output=args.output,
        api_key=args.api_key,
        prompt=args.prompt,
        format=args.output_format,
        language=args.language,
        translate=args.translate_to_english,
        run_whisper_locally=args.run_whisper_locally,
        local_whisper_options=local_whisper_options,
        font_options=font_options,
    )
    print(exit_message)
    return exit_code


def generate_captions(
    media: Path,
    output: Path,
    api_key: str = os.environ.get("OPENAI_API_KEY"),
    prompt: str = "",
    format: str = "srt",
    language: str = "en",
    translate: bool = False,
    run_whisper_locally: bool = False,
    local_whisper_options: dict = {
        "highlight_words": None,
        "highlight_color": None,
        "max_words_per_caption": None,
    },
    font_options: dict = {
        "font": None,
        "font_size": None,
    },
):
    if not output:
        output = media.with_suffix(f".{format}")

    if not media.is_file():
        exit_message = f"Media file {media} does not exist"
        return (1, exit_message)

    if any(local_whisper_options.values()):
        run_whisper_locally = True

    if not api_key and not run_whisper_locally:
        exit_message = (
            "OpenAI API key is required, none provided or found in environment"
        )
        return (1, exit_message)

    supported_formats = ["srt", "vtt"]
    if format not in supported_formats:
        exit_message = f"Output format {format} is not supported. Must be one of: {supported_formats}"
        return (1, exit_message)

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

    print(f"{transcribe_or_translate} using OpenAI's Whisper API to {format} format")

    do_transcribe(
        run_whisper_locally=run_whisper_locally,
        audio_to_transcribe=audio,
        caption_format=format,
        language=language,
        prompt=prompt,
        output_filename=output,
        api_key=api_key,
        api_transcribe_fn=transcribe,
        local_whisper_options=local_whisper_options,
    )

    # Post-process the captions
    if any(font_options.values()):
        if format == "vtt":
            print(
                "Font options are not supported for vtt format, request this feature on GitHub"
            )
        else:
            captions = pysrt.open(output)
            for caption in captions:
                if font_options["font"]:
                    caption.text = (
                        f"<font face='{font_options['font']}'>{caption.text}</font>"
                    )
                if font_options["font_size"]:
                    caption.text = f"<font size='{font_options['font_size']}'>{caption.text}</font>"
            captions.save(output)

    exit_message = f"Transcription complete, saved to {output}"
    return (0, exit_message)


def do_transcribe(
    run_whisper_locally: bool,
    audio_to_transcribe: Path,
    caption_format: str,
    language: str,
    prompt: str,
    output_filename: Path,
    api_key: str = None,
    api_transcribe_fn=None,
    local_whisper_options: dict = {},
):
    if run_whisper_locally:
        try:
            import stable_whisper
        except ImportError:
            print(
                "Dependencies to run Whisper locally are not installed,"
                + "please install them by running: "
                + "pip install -r requirements-advanced.txt"
            )
            raise

        model = stable_whisper.load_model("base")
        result = model.transcribe(
            str(audio_to_transcribe),
            initial_prompt=prompt,
        )

        max_words_per_caption = local_whisper_options["max_words_per_caption"]
        if max_words_per_caption and max_words_per_caption > 0:
            result = result.split_by_length(max_words=max_words_per_caption)

        color_tag = None
        if local_whisper_options["highlight_color"]:
            local_whisper_options["highlight_words"] = True
            color = local_whisper_options["highlight_color"]
            if color == "bold":
                color_tag = ("<b>", "</b>")
            else:
                color_tag = (f'<font color="{color}">', "</font>")

        result.to_srt_vtt(
            str(output_filename),
            word_level=local_whisper_options["highlight_words"],
            tag=color_tag,
            vtt=caption_format == "vtt",
        )
    else:
        openai.api_key = api_key
        with open(audio_to_transcribe, "rb") as f:
            transcript = api_transcribe_fn(
                "whisper-1",
                f,
                response_format=caption_format,
                language=language,
                prompt=prompt,
            )
        with open(output_filename, "w") as f:
            f.write(transcript)


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
