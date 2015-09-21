import multipartupload
import youcanhearme
import re
from nato import nato as nn
from nato import morse as mm

def saystuff(sentence):
    """Outputs a link to the aufio of the input."""
    sentence = sentence.encode('ascii', 'ignore') ##avoid unicode encode errors
    filename=youcanhearme.getsentence(sentence)
    s = multipartupload.upload(filename)
    url = re.search(r'(?<="Url":")(https://clyp.it/.*?)(?=")',s).group(0)
    return url

def abc(word):
    """Papa Yankee Tango Hotel Oscar November"""
    word = word.lower()
    letters = [nn[a] for a in word if a in nn.keys()]
    st = " ".join(letters)
    return st

def alphabet(sentence):
    """Alpha Romeo contingency"""
    output_list = []
    words = sentence.split(" ")
    for w in words:
        if w[0]==w[0].upper(): ##UPPERCASE?
            output_list.append(abc(w))
        else: ##lowercase
            output_list.append(w)
    st = " ".join(output_list)
    return st

def morse(sentence):
    sentence = sentence.lower()
    result = [mm[c] for c in sentence if c in mm.keys()]
    return " ".join(result)

def morsesound(sentence, freq=1000, length=100, path ='output\\'):
    """Turns a sentence into a morse soundfile"""
    mor = morse(sentence)
    from pydub.generators import Sine
    from pydub import AudioSegment
    import re

    dot = Sine(freq).to_audio_segment(length)
    dash =  Sine(freq).to_audio_segment(length*3)
    sil1 = AudioSegment.silent(length)
    sil3 = AudioSegment.silent(length*3)

    result = AudioSegment.silent(length)
    for a in mor:
        if a == ".":
            result += dot
        elif a == "-":
            result += dash
        elif a == "/":
            result += sil1
        else:
            result += sil3
        result += sil1

    filename = path + re.sub(r'[/\?!:*|",.]','',sentence) + '.mp3'
    result.export(filename,format="mp3")
    return filename

def morsestuff(sentence):
    """Upload a morse to clyp.it"""
    sentence = sentence.encode('ascii', 'ignore') ##avoid unicode encode errors
    filename = morsesound(sentence)
    s = multipartupload.upload(filename)
    url = re.search(r'(?<="Url":")(https://clyp.it/.*?)(?=")',s).group(0)
    return url
