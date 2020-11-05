import os
import pyttsx3
import requests
import googletrans
import PySimpleGUI as sg
import speech_recognition as sr


def language_translate(text, lang="id"):
    """ returns the text after it is translated """
    translator = googletrans.Translator()
    lang_convert = translator.translate(text, dest=lang)

    return lang_convert.text


def audio_to_text(audio):
    """ convert audio to text """
    recognizer = sr.Recognizer()
    sound = sr.AudioFile(audio)
    with sound as source:
        audio = recognizer.record(source)

    return recognizer.recognize_google(audio)


def text_to_audio(text):
    """ convert text into voice """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def check_internet():
    """ return true if internet is connect  """
    # google url only to test whether the user is connected to the internet
    url = "https://www.google.com/"
    timeout = 3
    try:
        requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        sg.popup("Lost Connection!")
        return False


def check_file(file):
    """ return true if parameter is file """
    if os.path.isfile(file):
        return True
    else:
        sg.popup("File Not Found!")
        return False


def layout():
    # audio column for layout
    audio_column = [
        [sg.InputText(key="File", size=(20, 0))],
        [sg.FileBrowse(target="File", size=(17, 0))],
        [sg.Button("Convert", size=(17, 0))],
        [sg.Button("Text", size=(17, 0))],
        [sg.Button("Voice", size=(17, 0))],
    ]

    # result column for layout
    result_column = [[sg.Output(size=(20, 10))]]

    # layout for window
    layout = [[sg.Column(audio_column), sg.VerticalSeparator(), sg.Column(result_column)]]

    # return window
    return sg.Window("Voice Translate", layout)


# create window
window = layout()

# flag for check file
allowed = False

# application loop
while check_internet():

    # read/get window event and values
    event, values = window.Read()

    # application closed if user click exit
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # check a user input if input is file/path
    if event == "Convert" and check_file(values["File"]):
        convert_to_text = audio_to_text(values["File"])
        text_translate = language_translate(convert_to_text)
        allowed = True

    if event == "Text" and allowed:
        # show text after translate
        print(text_translate)

    if event == "Voice" and allowed:
        # convert text after translate to voice and return it
        text_to_audio(text_translate)

# close application
window.close()
