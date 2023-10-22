# Phonix
Generate captions for videos using the power of OpenAI's Whisper API

## What?

Phonix is a Python program that uses OpenAI's API to generate captions for videos.

It uses the [Whisper](https://platform.openai.com/docs/models/whisper) model,
an automatic speech recognition system that can turn audio into text and potentially translate it too.
Compared to other solutions, it has the advantage that its transcription can be "enhanced"
by the user providing prompts that indicate the "domain" of the video.
This means you may get better results if you use technical terms, acronyms and jargon.

## Why?

Captions are not just for the hearing impaired.
They make your content more engaging by boosting your audience's focus, attention and
comprehension while allowing them to watch your video without sound.

I was not particularly satisfied with the accuracy of Youtube's and Linkedin's automatic captions
so I gave Whisper a try and was impressed by the results.
Phonix makes it easy to use Whisper and generate captions for your videos.

## How?

Phonix first extracts the audio from the video, then downsamples it in case it's over 25 MB
and finally sends it to OpenAI's Whisper API.
The API returns the captions in the specified format and Phonix saves them to a file.
You can then use the captions in your video editor of choice.

Phonix was originally a command line application but I thought it'd be cool to create a simple
GUI for it. Use whichever you feel more comfortable with.

### Installation

* Get an [OpenAI API key](https://platform.openai.com/account/api-keys)
  * This is a paid service and a 25 minute South Park episode cost me around $0.30 to transcribe
* Clone or download this repository
* Install a recent version of Python with [Tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
* Install `ffmpeg` [for your platform](https://ffmpeg.org/download.html)
* Install Python dependencies: `pip install -r requirements-basic.txt`

### Command line usage

`phonix.py` is the command line interface that also includes the main logic of the program.<br>
It has a few options that you can see by running `python phonix.py --help`.

### GUI usage

Assuming you have installed the dependencies, you can run the GUI with `python phonix_gui.py`.
A demo of the tool can be found in this [video](https://youtu.be/kkJzt00qafo).
