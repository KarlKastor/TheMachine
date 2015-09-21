from bs4 import BeautifulSoup
##from glob import iglob
from pydub import AudioSegment
import os,random,shutil
##import httplib,urllib
import urllib2
##text=urllib2.urlopen("http://www.dict.cc/?s=can").read()
import requests, re
##from pydub import AudioSegment
##httplib.HTTPConnection.debuglevel = 1

sound_dir = 'sounds\\'
temp_dir = 'temp\\'
out_dir = 'output\\'
rep_dir = 'replace\\'
lang = 'en'
ill_chars='/\?!:*|",.'

user_agent = {'User-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}

def getwordaudio(word):
    url= "http://www.dict.cc/?s=" + word
    text = requests.get(url,headers=user_agent).text
    ##soup = BeautifulSoup(text)

    if not 'Array' in text:
        return 0

    n=re.search(r'(?:Array\(0,)(.*?)\)',text).group()
    numbers = re.split(',',n[n.find('(')+1:-1])

    w = re.search(r'(?:var c1Arr = new Array\()(.*?)(\))',text).group().replace(r'"','')
    words = re.split(",",w[w.find("(")+1:-1])

    if word in words or word.lower() in words:
        ID = random.choice([i for i in range(len(words)) if words[i].lower()==word.lower()]) ##the index of something that equals the word
        ##ID = str(words.index(word))
    elif 'to ' + word in words:
        ID = random.choice([i for i in range(len(words)) if words[i]=='to ' + word])
    else:
        ID = 1;
    audio_url = 'http://audio.dict.cc/speak.audio.php?type=mp3&id='+numbers[ID]+'&lang='+lang+'_rec_ip&lp=DEEN'
    #return requests.get(audio_url,headers=user_agent)
    return audio_url

def getwordaudio2(word):
    url= "http://forvo.com/word/" + word
    text = requests.get(url,headers=user_agent).text
    soup = BeautifulSoup(text, "lxml")

    ##get the first list of pronunciation (Usally the en one)
    soup = soup.find("article",attrs={'class':'pronunciations'})
    ar = soup.findAll("a", title="Listen {} pronunciation".format(word.lower()))

    numbers = [a.get("id").replace("play_","") for a in ar]
    if len(numbers)==0:
        return 0
    n = random.choice(numbers)

    js_url = "http://forvo.com/_ext/ext-prons.js?id="
    js_text = requests.get(js_url + n,headers=user_agent).text

    audio_url = re.search(r"http://apifree.*?(?=\\',)",js_text).group()
    
    return audio_url
    
def savewordaudio(u,file_name):
    req = urllib2.Request(u)
    req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0")
    f = open(file_name,'wb')
    f.write(urllib2.urlopen(req).read())
    f.close()

def getsentence(s):
    s = s.lower()
    s = re.sub(r'[%s]'%ill_chars,'',s)
    s = s.replace(r'’',"'")
    words = re.split('[ \.]',s)
    for z in range(len(words)):
        ##print 'ZZZZZZZZZZZZZ' + str(z)
        a=words[z]
        
        ##is the word saved because of problems with the online sound
        if os.path.isfile(rep_dir + a + '0.mp3'):
            e = 1
            while os.path.isfile(rep_dir + str(e) + '.mp3'):
                e += 1
            ##a random one of the e+1 replacements is copied
            shutil.copy(rep_dir + a + str(random.randint(0,e)) + '.mp3',temp_dir + str(z)+ '.mp3')
                
        ##a error or intended silence    
        elif a == ' ' or a == '':
            shutil.copy(sound_dir + 'silence.mp3',temp_dir + str(z)+ '.mp3')

        ##download
        else:
            link=getwordaudio(a)
            ##word not found akward silence instead
            if not link:
                shutil.copy(sound_dir + 'silence.mp3',temp_dir + str(z)+ '.mp3')
            ##normal download
            else:
                savewordaudio(link,temp_dir + str(z)+ '.mp3')
            
##            f = open(temp_dir + str(z)+ ".mp3","wb")
##            f.write(open(sound_dir + "endbeep.mp3","rb").read())
##            f.close()
    ##AudioSegment.converter = "C:\\FFMPEG\\bin\\ffmpeg.exe"          
    startbeep = AudioSegment.from_mp3(sound_dir + 'startbeep.mp3')
    #startbeep = startbeep.apply_gain(+5.5)
    endbeep = AudioSegment.from_mp3(sound_dir + 'endbeep.mp3')
    #endbeep = endbeep.apply_gain(+6.5)
    noise = AudioSegment.from_mp3(sound_dir + 'noise.mp3')
    noise = noise.apply_gain(-10.5)
    every_word = [AudioSegment.from_mp3(temp_dir + str(i)+ '.mp3') for i in range(len(words))]
    out = startbeep
    for e in every_word:
        out = out.append(e.apply_gain(10.5))
    ##out = out.strip_silence(silence_len=1000, silence_thresh=-100, padding=-200)
    out = out.append(endbeep)
    out = out.overlay(noise, loop=1)
    if len(s)>100:
        s=s[:99]
    filename=out_dir + s + '.mp3'
    out.export(filename, format='mp3').close()
    return filename
    
##    fi = open(out_dir + s+".mp3", "wb")
##    shutil.copyfileobj(open(sound_dir + "startbeep.mp3","rb"),fi)
##    for z in range(len(words)):
##        ##o=open(
##        shutil.copyfileobj(open(temp_dir + str(z)+".mp3","rb"),fi)
##        ##fi.write(o.read())
##        ##o.close()
##    ##shutil.copyfileobj(open(sound_dir + "endbeep.mp3","rb"),fi)
##    shutil.copyfileobj(open(sound_dir + "endbeep.mp3","rb"),fi)
##    fi.close()

            
##    fi = open(out_dir + s+".mp3", "wb")
##    shutil.copyfileobj(open(sound_dir + "startbeep.mp3","rb"),fi)
##    for z in range(len(words)):
##        ##o=open(
##        shutil.copyfileobj(open(temp_dir + str(z)+".mp3","rb"),fi)
##        ##fi.write(o.read())
##        ##o.close()
##    ##shutil.copyfileobj(open(sound_dir + "endbeep.mp3","rb"),fi)
##    shutil.copyfileobj(open(sound_dir + "endbeep.mp3","rb"),fi)
##    fi.close()
    
##    sen = AudioSegment.from_mp3("0.mp3")
##    for z in range(1,len(words)):
##        if words[z]==" ":
##            continue
##        sen += AudioSegment.from_mp3(z + ".mp3")
##    sen.export(s+".mp3")
        
