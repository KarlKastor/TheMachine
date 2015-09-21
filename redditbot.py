import time
import re

import praw
import botpw
import machinetools
import face_detect

keyword = "/u/poi_machine"

text_audio = \
"""[!]./audio.INITIALIZE

//UPLOAD_AUDIO [DONE]

[//SEND_LINK [DONE]]({})"""

text_face = \
"""[!]./faces.FIND

//UPLOAD_IMAGE [DONE]

[//SEND_LINK [DONE]]({})"""


def answer(comment):
    """Answers given comment."""
    text = comment.body.replace("\n","")
    low = text.lower()
    print "//INCOMING COMMENT {}: {}".format(comment.id, text)
    
    if keyword not in text.lower():
        print "//KEYWORD NOT IN COMMENT"
        return
    
    if keyword + " say " in low:
        m = re.search(keyword + " say ", text, flags=re.IGNORECASE)
        say = text[m.end(0):]
        say = machinetools.alphabet(say).encode('ascii', 'ignore')
        url = machinetools.saystuff(say)
        message = text_audio.format(url)
        comment.reply(message)
        return
    
    if keyword + " morse " in low:
        m = re.search(keyword + " morse ",text, flags=re.IGNORECASE)
        say = text[m.end(0):].encode('ascii', 'ignore')
        url = machinetools.morsestuff(say)
        message = text_audio.format(url)
        comment.reply(message)
        return

    img_pattern = "(?<={} )(https?://.*?\.(?:jpe?g|png|bmp)) (.*)".format(keyword)
    m = re.search(img_pattern, text, flags=re.I)
    if m:
        try:
            url = face_detect.from_url(m.group(1), m.group(2))
            message = text_face.format(url)
        except:
            message = "//AN ERROR OCURRED WITH THE IMAGE!"
        comment.reply(message)
        return
         
    comment.reply("0000000")
    print "ERROR 0000000 at {}".format(comment.id)
        
def main():
    global r
    print "//REDDIT.login... [IN PROGRESS]"
    r = praw.Reddit('/u/KarlKastor testing around with stuff')
    r.set_oauth_app_info(client_id=botpw.cid, client_secret=botpw.cs, redirect_uri='https://127.0.0.1:65010/authorize_callback')
    refreshed = r.refresh_access_information(botpw.ai['refresh_token'])
    r.set_access_credentials(**refreshed)
    print "//REDDIT.login [COMPLETE]"
    seen = [] ##list of seen comments because unread apparently has a delay
    while True:
        print "//CHECKING_INCOMING_DATA_FEEDS [IN PROGRESS]"
        for c in r.get_unread():
            try:
                if not c.id in seen:
                    answer(c)
                    print "//ANSWERED {}".format(c.id)
            except praw.errors.RateLimitExceeded as err:
                print err
                print "//WAITING 10 MINUTES"
                for i in range(10*60):
                    time.sleep(1)  
            except Exception as err:
                print err, c.id
                time.sleep(20)              
            finally:
                seen.append(c.id)
                c.mark_as_read()
        time.sleep(5)
        

if __name__ == "__main__":
    main()
        
    
    ##r.submit(subreddit,'Test',"so that's working")

##while True:
##    name= raw_input("Name: ")
##    try:
##        r.get_redditor(name)
##        print "Taken"
##    except:
##        print "Not Taken"
##
##    if name=="exit":
##        break
