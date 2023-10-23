#!/usr/bin/env python3
"""
The GUI for phonix.py
"""

import phonix
import sys
import PySimpleGUI as sg
import os.path

from pathlib import Path


def main():
    sg.theme("DarkBlack")

    top_row = [sg.Text("Phonix", font=("Helvetica", 25), justification="center")]

    # Media file
    select_media_file = [
        sg.Text(
            "Select media file",
            font=("Helvetica", 20),
            justification="left",
            key="media_file_title",
        )
    ]
    media_file_input = [
        sg.InputText(key="media_file", size=(50, 1), enable_events=True),
        sg.FileBrowse(),
    ]
    media_file = [select_media_file, media_file_input]

    # Output file
    select_output_file = [
        sg.Text(
            "Select output file destination",
            font=("Helvetica", 20),
            justification="left",
            key="output_file_title",
        )
    ]
    output_file_input = [
        sg.InputText(key="output_file", size=(50, 1)),
        sg.FileSaveAs(button_text="Save as"),
        sg.Button(
            "X",
            key="reset_output_file",
            tooltip="Reset output file to default",
            enable_events=True,
        ),
    ]
    output_file = [select_output_file, output_file_input]

    # API key
    select_api_key = [
        sg.Text(
            "Select OpenAI API key",
            font=("Helvetica", 20),
            justification="left",
            key="api_key_title",
        )
    ]
    api_key_input = [
        sg.InputText(
            key="api_key",
            size=(50, 1),
            default_text=os.environ.get("OPENAI_API_KEY"),
            enable_events=True,
        )
    ]
    run_whisper_locally = [
        sg.Checkbox(
            "Run Whisper locally",
            key="run_whisper_locally",
            enable_events=True,
            background_color="gray",
            tooltip="Run Whisper locally instead of using the OpenAI API."
            + "Select this if you want to highlight specific words "
            + "or limit the number of words per caption.",
        )
    ]
    api_key = [select_api_key, api_key_input, run_whisper_locally]

    # Prompt
    select_prompt = [
        sg.Text(
            "Select prompt",
            font=("Helvetica", 20),
            justification="left",
            key="prompt_title",
        )
    ]
    prompt_type = [
        sg.Radio(
            "String",
            "prompt_type",
            key="prompt_string",
            default=True,
            enable_events=True,
        ),
        sg.Radio("File", "prompt_type", key="prompt_file", enable_events=True),
    ]
    prompt_file_input = [
        sg.InputText(key="prompt_file_input", size=(50, 1), disabled=True),
        sg.FileBrowse(disabled=True, key="prompt_file_input_browse"),
    ]
    prompt_string_input = [sg.Multiline(key="prompt_string_input", size=(50, 5))]
    prompt = [select_prompt, prompt_type, prompt_string_input, prompt_file_input]

    # Captions format
    select_captions_format = [
        sg.Text(
            "Select captions format",
            font=("Helvetica", 20),
            justification="left",
            key="captions_format_title",
        )
    ]
    captions_format_options = [
        sg.Radio(
            ".srt",
            "captions_format",
            key="captions_format_srt",
            default=True,
        ),
        sg.Radio(".vtt", "captions_format", key="captions_format_vtt"),
    ]
    # Captivating captions
    captivating_captions = [
        sg.Text(
            "Captivating captions",
            font=("Helvetica", 20),
            justification="left",
            key="captivating_captions_title",
        )
    ]
    highlight_words = [
        sg.Checkbox(
            "Highlight words",
            key="highlight_words",
            background_color="gray",
            tooltip="Highlight the spoken word",
        )
    ]
    highlight_color = [
        sg.Text("Highlight color:"),
        sg.Combo(
            [
                None,
                "bold",
                "red",
                "green",
                "blue",
                "yellow",
                "magenta",
                "cyan",
                "white",
            ],
            default_value=None,
            key="highlight_color",
            enable_events=True,
            readonly=True,
        ),
    ]
    max_words_per_caption = [
        sg.Text("Max words per caption:"),
        sg.InputText(
            key="max_words_per_caption",
            enable_events=True,
            size=(2, 1),
        ),
    ]
    # Font type
    font_type = [
        sg.Text("Font type:"),
        sg.InputText(
            key="font_type",
            size=(20, 1),
            default_text="",
        ),
    ]
    # Font size
    font_size = [
        sg.Text("Font size:"),
        sg.InputText(
            key="font_size",
            size=(3, 1),
            default_text="",
            enable_events=True,
        ),
    ]

    captions_format = [
        select_captions_format,
        captions_format_options,
        captivating_captions,
        highlight_words,
        highlight_color,
        max_words_per_caption,
        font_type,
        font_size,
    ]

    # Transcribe or translate
    select_transcribe_or_translate = [
        sg.Text(
            "Transcribe or Translate",
            font=("Helvetica", 20),
            justification="left",
            key="transcribe_or_translate_title",
        )
    ]
    transcribe_or_translate_radio = [
        sg.Radio(
            "Transcribe",
            "transcribe_or_translate",
            key="transcribe",
            default=True,
            enable_events=True,
        ),
        sg.Radio(
            "Translate", "transcribe_or_translate", key="translate", enable_events=True
        ),
    ]
    transcribe_or_translate = [
        select_transcribe_or_translate,
        transcribe_or_translate_radio,
    ]

    # Language
    select_language = [
        sg.Text(
            "Select input media language",
            font=("Helvetica", 20),
            justification="left",
            key="language_title",
        )
    ]
    ## Available languages in ISO 639-1 format:
    # Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian,
    # Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish,
    # French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian,
    # Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, North Macedonian,
    # Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian,
    # Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil,
    # Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh
    language_dropdown = [
        sg.Combo(
            [
                "Afrikaans (af)",
                "Arabic (ar)",
                "Armenian (hy)",
                "Azerbaijani (az)",
                "Belarusian (be)",
                "Bosnian (bs)",
                "Bulgarian (bg)",
                "Catalan (ca)",
                "Chinese (zh)",
                "Croatian (hr)",
                "Czech (cs)",
                "Danish (da)",
                "Dutch (nl)",
                "English (en)",
                "Estonian (et)",
                "Finnish (fi)",
                "French (fr)",
                "Galician (gl)",
                "German (de)",
                "Greek (el)",
                "Hebrew (he)",
                "Hindi (hi)",
                "Hungarian (hu)",
                "Icelandic (is)",
                "Indonesian (id)",
                "Italian (it)",
                "Japanese (ja)",
                "Kannada (kn)",
                "Kazakh (kk)",
                "Korean (ko)",
                "Latvian (lv)",
                "Lithuanian (lt)",
                "North Macedonian (mk)",
                "Malay (ms)",
                "Marathi (mr)",
                "Maori (mi)",
                "Mongolian (mn)",
                "Nepali (ne)",
                "Norwegian (no)",
                "Persian (fa)",
                "Polish (pl)",
                "Portuguese (pt)",
                "Romanian (ro)",
                "Russian (ru)",
                "Serbian (sr)",
                "Slovak (sk)",
                "Slovenian (sl)",
                "Spanish (es)",
                "Swahili (sw)",
                "Swedish (sv)",
                "Tagalog (tl)",
                "Tamil (ta)",
                "Thai (th)",
                "Turkish (tr)",
                "Ukrainian (uk)",
                "Urdu (ur)",
                "Vietnamese (vi)",
                "Welsh (cy)",
            ],
            default_value="English (en)",
            key="language",
            readonly=True,
        )
    ]
    language = [select_language, language_dropdown]

    # Bottom navigation buttons
    bottom_navigation = [
        sg.Button("Previous", key="previous", disabled=True),
        sg.Button("Next", key="next", disabled=True),
        sg.Button("Transcribe", key="run", disabled=True),
    ]

    # TODO: Turn this into a list and skip the next and previous fields?
    transitions = {
        "media_file": {
            "current": "media_file",
            "next": "api_key",
            "previous": None,
        },
        "api_key": {
            "current": "api_key",
            "next": "prompt",
            "previous": "media_file",
        },
        "prompt": {
            "current": "prompt",
            "next": "captions_format",
            "previous": "api_key",
        },
        "captions_format": {
            "current": "captions_format",
            "next": "output_file",
            "previous": "prompt",
        },
        "output_file": {
            "current": "output_file",
            "next": "transcribe_or_translate",
            "previous": "captions_format",
        },
        "transcribe_or_translate": {
            "current": "transcribe_or_translate",
            "next": "language",
            "previous": "output_file",
        },
        "language": {
            "current": "language",
            "next": None,
            "previous": "transcribe_or_translate",
        },
    }

    current_transition = transitions["media_file"]
    layout = [
        top_row,
        [sg.HorizontalSeparator()],
        [
            sg.Column(
                media_file,
                key="media_file_column",
                size=(500, 300),
            ),
            sg.Column(
                api_key,
                key="api_key_column",
                visible=False,
                size=(500, 300),
            ),
            sg.Column(
                prompt,
                key="prompt_column",
                visible=False,
                size=(500, 300),
            ),
            sg.Column(
                captions_format,
                key="captions_format_column",
                visible=False,
                size=(500, 300),
            ),
            sg.Column(
                output_file,
                key="output_file_column",
                visible=False,
                size=(500, 300),
            ),
            sg.Column(
                transcribe_or_translate,
                key="transcribe_or_translate_column",
                visible=False,
                size=(500, 300),
            ),
            sg.Column(
                language,
                key="language_column",
                visible=False,
                size=(500, 300),
            ),
        ],
        [sg.HorizontalSeparator()],
        bottom_navigation,
    ]

    window = sg.Window("Phonix", layout)
    previous_max_words_per_caption = ""
    previous_font_size = ""
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "next":
            # Showing next transition logic
            current_transition_key = current_transition["current"]
            window[current_transition_key + "_column"].update(visible=False)

            next_transition_key = transitions[current_transition_key]["next"]
            next_transition = transitions[next_transition_key]
            window[next_transition_key + "_column"].update(visible=True)
            current_transition = next_transition
            current_transition_key = next_transition_key

            # Bottom navigation logic
            if not current_transition["next"]:
                window["next"].update(disabled=True)
                window["run"].update(disabled=False)
            else:
                window["next"].update(disabled=False)
                window["run"].update(disabled=True)
            window["previous"].update(disabled=False)

            # Specific logic for each transition
            if current_transition_key == "api_key":
                if values["api_key"] or values["run_whisper_locally"]:
                    window["next"].update(disabled=False)
                else:
                    window["next"].update(disabled=True)
            elif current_transition_key == "output_file":
                assert values["media_file"]  # By now it should be a valid path
                # In case the user has already selected a file, we don't want to overwrite it
                format = "srt" if values["captions_format_srt"] else "vtt"
                if values["output_file"]:
                    current_output_file = Path(values["output_file"])
                    current_output_file = current_output_file.with_suffix(f".{format}")
                    window["output_file"].update(value=current_output_file)
                else:
                    input_media_file = Path(values["media_file"])
                    default_output_file = input_media_file.with_suffix(f".{format}")
                    window["output_file"].update(value=default_output_file)

        elif event == "previous":
            current_transition_key = current_transition["current"]
            window[current_transition_key + "_column"].update(visible=False)

            previous_transition_key = transitions[current_transition_key]["previous"]
            previous_transition = transitions[previous_transition_key]
            window[previous_transition_key + "_column"].update(visible=True)
            current_transition = previous_transition

            if not current_transition["previous"]:
                window["previous"].update(disabled=True)
            else:
                window["previous"].update(disabled=False)

            window["next"].update(disabled=False)
            window["run"].update(disabled=True)
        elif event == "media_file":
            try:
                if Path(values["media_file"]).is_file():
                    window["next"].update(disabled=False)
                else:
                    window["next"].update(disabled=True)
            except Exception:
                pass
        elif event == "api_key":
            if values["api_key"]:
                window["next"].update(disabled=False)
            else:
                window["next"].update(disabled=True)
        elif event == "run_whisper_locally":
            if values["run_whisper_locally"]:
                window["api_key"].update(disabled=True)
                window["next"].update(disabled=False)
            else:
                window["api_key"].update(disabled=False)
                if values["api_key"]:
                    window["next"].update(disabled=False)
                else:
                    window["next"].update(disabled=True)
        elif event == "max_words_per_caption":
            # Only allow numbers and values between up to 20
            max_words_value = values["max_words_per_caption"]
            if max_words_value != "":
                if (
                    str(max_words_value).isnumeric()
                    and int(max_words_value) > 0
                    and int(max_words_value) <= 20
                ):
                    previous_max_words_per_caption = int(max_words_value)
                else:
                    window["max_words_per_caption"].update(
                        value=previous_max_words_per_caption
                    )
            else:
                previous_max_words_per_caption = values["max_words_per_caption"]
        elif event == "font_size":
            # Only allow numbers and values between up to 999
            font_size_value = values["font_size"]
            if font_size_value != "":
                if (
                    str(font_size_value).isnumeric()
                    and int(font_size_value) > 0
                    and int(font_size_value) <= 999
                ):
                    previous_font_size = int(font_size_value)
                else:
                    window["font_size"].update(value=previous_font_size)
            else:
                previous_font_size = values["font_size"]
        elif event == "highlight_color":
            window["highlight_words"].update(value=values["highlight_color"] != None)
        elif event == "prompt_string":
            window["prompt_string_input"].update(disabled=False)
            window["prompt_file_input"].update(disabled=True, value="")
            window["prompt_file_input_browse"].update(disabled=True)
        elif event == "prompt_file":
            window["prompt_string_input"].update(disabled=True, value="")
            window["prompt_file_input"].update(disabled=False)
            window["prompt_file_input_browse"].update(disabled=False)
        elif event == "reset_output_file":
            input_media_file = Path(values["media_file"])
            default_output_file = input_media_file.with_suffix(f".{format}")
            window["output_file"].update(value=default_output_file)
        elif event == "translate":
            window["run"].update(text="Translate")
            # Input language is automatically detected, only translation to English is supported
            window["language"].update(disabled=True, value="English (en)")
        elif event == "transcribe":
            window["run"].update(text="Transcribe")
            window["language"].update(disabled=False)
        elif event == "run":
            media_path = Path(values["media_file"])
            format_value = "srt" if values["captions_format_srt"] else "vtt"
            output_file_path = Path(values["output_file"]).with_suffix(
                f".{format_value}"
            )
            api_key_value = values["api_key"]
            # Either the prompt string or file are empty so it's safe to concatenate them
            prompt_value = values["prompt_string_input"] + values["prompt_file_input"]
            # Language is in form "English (en)" so we need to extract the code
            language_value = (
                values["language"].split(" ")[-1].replace("(", "").replace(")", "")
            )
            translate_value = values["translate"]
            run_whisper_locally_value = values["run_whisper_locally"]
            max_words_per_caption_value = (
                int(values["max_words_per_caption"])
                if str(values["max_words_per_caption"]).isnumeric()
                else None
            )
            local_whisper_options = {
                "highlight_words": values["highlight_words"],
                "highlight_color": values["highlight_color"],
                "max_words_per_caption": max_words_per_caption_value,
            }

            font_options = {
                "font": values["font_type"],
                "font_size": int(values["font_size"]),
            }

            exit_code, exit_message = phonix.generate_captions(
                media=media_path,
                output=output_file_path,
                api_key=api_key_value,
                prompt=prompt_value,
                format=format_value,
                language=language_value,
                translate=translate_value,
                run_whisper_locally=run_whisper_locally_value,
                local_whisper_options=local_whisper_options,
                font_options=font_options,
            )
            popup = sg.popup_ok if exit_code == 0 else sg.popup_error
            popup(exit_message)

    window.close()


if __name__ == "__main__":
    sys.exit(main())
