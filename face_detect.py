import sys
import urllib
import cv2
from PIL import Image
from imgurpython import ImgurClient
from botpw import i

client = ImgurClient(*i)

cascPath = "cascade.xml"
boxPath = "boxes\\"

output_dir = "output\\"

def from_url(url,boxes=None):
    if boxes is None:
        boxes = []
    imagePath, _ = urllib.urlretrieve(url)
    filename = output_dir + imagePath[imagePath.rfind("\\")+1:]
    irr(imagePath,boxes,filename)
    d = client.upload_from_path(filename, config=None, anon=True)
    return d["link"]

def irr(imagePath,boxes=None,filename="output.jpg"):
    """adds the boxes to the faces"""


    
    ##detect faces and sort them left to right
    faces = sorted(detect_faces(imagePath),key= lambda x: x[0])

    if not boxes:
        boxes = ["irrelevant"]*len(faces)
        
    if "," in boxes:
        boxes = boxes.replace(" ","").lower().split(",")
    elif " " in boxes:
        boxes = boxes.lower().split(" ")
    else:
        boxes = [boxes]

    ##if not enough boxes are specified, fill it up with irrelevant
    if len(boxes)==0:
        boxes+=["irrelevant"]*len(faces)

    im = Image.open(imagePath)

    ##add the recticle for each face
    for (x,y,w,h),b in zip(faces,boxes):
        ##choose the wanted box as filename
        if b in ["admin","yellow","contingency","a","y","c"]:
            boxName = "yellow.png"
        elif b in ["threat","red","t","r"]:
            boxName = "red.png"
        elif b in ["indigo","blue","b"]:
            boxName = "indigo.png"
        elif b in ["irrelevant","white","grey","normal","i","w","g","n"]:
            boxName = "white.png"
        elif b in ["root","analog_interface","interface","ai"]:
            boxName = "ai.png"
        
        else:
            boxName = "blank.png"

        if boxName != "blank.png":
            ##load the reticle and downsize it
            box = Image.open(boxPath + boxName)
            f = 1.5 ##scale factor to mark the whole head
            s = (w if w>h else h)*f
            box.thumbnail((s,s), Image.ANTIALIAS)
            x,y = int(x - (s-w)//2) , int(y - (s-h)//1.5)
            ##print x,y

            ##put the reticle over the original image
            im.paste(box, (x, y),box)

    im.save(filename,quality=95)
          

def detect_faces(imagePath):
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    im = cv2.imread(imagePath,1)
    ##h, w = im.shape[:2]
     
    ##im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        im,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))

    return faces

##    # Draw a rectangle around the faces
##    for (x, y, w, h) in faces:
##        print x,y,w,h
##        cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
##
##    cv2.imshow("Faces found", im)
##    cv2.waitKey(0)
