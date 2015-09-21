# -*- coding: cp1252 -*-
nato = \
{'a': 'Alpha',
 'b': 'Bravo',
 'c': 'Charlie',
 'd': 'Delta',
 'e': 'Echo',
 'f': 'Foxtrot',
 'g': 'Golf',
 'h': 'Hotel',
 'i': 'India',
 'j': 'Juliet',
 'k': 'Kilo',
 'l': 'Lima',
 'm': 'Mike',
 'n': 'November',
 'o': 'Oscar',
 'p': 'Papa',
 'q': 'Quebec',
 'r': 'Romeo',
 's': 'Sierra',
 't': 'Tango',
 'u': 'Uniform',
 'v': 'Victor',
 'w': 'Whiskey',
 'x': 'X-ray',
 'y': 'Yankee',
 'z': 'Zulu'}

morse = \
{' ': '/',
 "'": '.----.',
 '(': '-.--.',
 ')': '-.--.-',
 '+': '.-.-.',
 ',': '--..--',
 '-': '-....-',
 '.': '.-.-.-',
 '/': '-..-.',
 '0': '-----',
 '1': '.----',
 '2': '..---',
 '3': '...--',
 '4': '....-',
 '5': '.....',
 '6': '-....',
 '7': '--...',
 '8': '---..',
 '9': '----.',
 ':': '---...',
 ';': '-.-.-.',
 '=': '-...-',
 '?': '..--..',
 '@': '.--.-.',
 'ch': '----',
 'a': '.-',
 'b': '-...',
 'c': '-.-.',
 'd': '-..',
 'e': '.',
 'f': '..-.',
 'g': '--.',
 'h': '....',
 'i': '..',
 'j': '.---',
 'k': '-.-',
 'l': '.-..',
 'm': '--',
 'n': '-.',
 'o': '---',
 'p': '.--.',
 'q': '--.-',
 'r': '.-.',
 's': '...',
 't': '-',
 'u': '..-',
 'v': '...-',
 'w': '.--',
 'x': '-..-',
 'y': '-.--',
 'z': '--..',
 'à': '.--.-',
 'ä': '.-.-',
 'å': '.--.-',
 'è': '.-..-',
 'é': '..-..',
 'ñ': '--.--',
 'ö': '---.',
 'ü': '..--',
 'ß': '...--..'}

reverse_morse = {v: k for k, v in morse.items()}

##def find(m, t=""):
##    if len(m)<1:
##        print t
##    else:
##        for i in range(1,len(m)+1):
##            if m[:i] in reverse_morse.keys():
##                find(m[i:],t+reverse_morse[m[:i]])
##
##def chars(m):
##    for j in range(0,len(m)+1):
##        print "\n",
##        for i in range(j,len(m)+1):
##            if m[j:i] in reverse_morse.keys():
##                print reverse_morse[m[j:i]], 
