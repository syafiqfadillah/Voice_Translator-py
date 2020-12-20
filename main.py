import os
import gtts
import playsound
import requests
import googletrans
import PySimpleGUI as sg
import speech_recognition as sr


def language_translate(text, lang):
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


def text_to_audio(text, lang, audio_name):
    """ convert text into voice """
    convert_text = gtts.gTTS(text=text, lang=lang, slow=True)
    convert_text.save(f"{audio_name}.mp3")


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
    """ return true if argument is file """
    if os.path.isfile(file):
        return True
    else:
        sg.popup("File Not Found!")
        return False


def check_file_extension(file):
    """ returns true if argument has a .wav extension """
    if file.lower().endswith(".wav"):
        return True
    else:
        sg.popup("The File Type Is Not .wav!")
        return False


def languages():
    """ returns a dict of languages"""
    lang = googletrans.LANGUAGES

    # set up new keys
    new_keys = dict(map(reversed, lang.items()))

    return new_keys


def play_audio(audio_name):
    """ play audio after it is translated """
    playsound.playsound(f"{audio_name}.mp3")


def layout():

    list_languages = list(all_lang.keys())

    # setting column for layout
    setting_column = [
        [sg.Text("File Path : ", size=(20, 0))],
        [sg.InputText(key="File", size=(20, 0))],
        [sg.FileBrowse(target="File", size=(17, 0))],
        [sg.Text("Audio Name : ", size=(20, 0))], 
        [sg.InputText(key="AudioName", size=(20, 0))],
        [sg.Text("Languages : ", size=(10, 0))], 
        [sg.Combo(list_languages, key="Languages", size=(10, 5))],
    ]

    # convert column for layout 
    convert_column = [
        [sg.Text("First Convert : ")],
        [sg.Button("Convert", size=(17, 0))],
        [sg.Text("Convert To Text : ")],
        [sg.Button("Text", size=(17, 0))],
        [sg.Text("Convert To Audio : ")],
        [sg.Button("Voice", size=(17, 0))]
    ]

    # result column for layout
    result_column = [[sg.Output(size=(20, 10))]]

    # layout for window
    create_layout = [[sg.Column(setting_column), sg.VerticalSeparator(), 
                      sg.Column(convert_column), sg.VerticalSeparator(), sg.Column(result_column)]]

    # return window
    return sg.Window("Voice Translate", create_layout)


all_lang = languages()

# create window
window = layout()

# flag for check file
allowed = False

# application loop
while check_internet():

    # read/get window event and values
    event, values = window.Read()

    # application closed if user click exit
    if event in ("Exit", sg.WIN_CLOSED):
        break

    # check a user input if input is file/path
    if (event == "Convert" and check_file(values["File"])) and check_file_extension(values["File"]):
        convert_to_text = audio_to_text(values["File"])
        text_translate = language_translate(convert_to_text, values["Languages"])
        allowed = True

    if event == "Text" and allowed:
        # show text after translate
        print(text_translate)

    if event == "Voice" and allowed:
        # convert text after translate to voice and return it
        text_to_audio(text_translate, all_lang[values["Languages"]], values["AudioName"])
        play_audio(values["AudioName"])

# close application
window.close()
