from orbit import ISS
from pathlib import Path
from numpy import random  # placeholder
from datetime import datetime, timedelta, timezone
from picamera import PiCamera
from logzero import logger, logfile
from time import sleep
import csv
from PIL import Image
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file


def getLocation():
    #gets the latitude andlongitude of the ISS
    location = ISS.coordinates()
    latitude = location.latitude.degrees
    longitude = location.longitude.degrees
    return(latitude, longitude)


def CreateCSV(dataFile):
    #creates a CSV file
    with open(dataFile, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter","Date/Time", "Latitude", "Longitude",
        "Classification","Classification probability", "ImageName")
        writer.writerow(header)


def AddData(dataFile, data):
    #adds data to the CSV file
    with open(dataFile, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def takePhoto(counter):
    picName = "IMG"+str(counter).zfill(3)+".jpg"
    picFile = f"{script_dir}/{picName}"
    camera.capture(picFile)
    return(picName)


def classification(picName):

    image_file = picName
    image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)
    common.set_input(interpreter,image)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)
    labels = read_label_file(label_file)
    for c in classes:
        return(f'{labels.get(c.id, c.id)}',f'{c.score:.5f}')


#initialize AI
script_dir = Path(__file__).parent.resolve()
model_file = script_dir/'astropi-land-vs-sea.tflite'
label_file = script_dir/'data/land-vs-sea.txt'
interpreter = make_interpreter(f"{model_file}")
interpreter.allocate_tensors()
size = common.input_size(interpreter)

# set up CSV
dataFile = script_dir/"data.csv"
CreateCSV(dataFile)

# set up logfile, which collects the data in a harder to understand
# format but will stay there if the program is restarted and holds
# errors.
logfile(script_dir/"events.log")

# set up camera
camera = PiCamera()

# nearly 3hr loop
start = datetime.now(timezone.utc)
timeNow = datetime.now(timezone.utc)

counter = 0
#change this to test faster
gapSecs = 30

while (timeNow < start+timedelta(minutes=178)):
    try:
        #add the data
        loc = getLocation()
        picName = takePhoto(counter)
        classified = classification(picName)
        data = (
            str(counter).zfill(3),
            timeNow.isoformat(), 
            loc[0], 
            loc[1], 
            classified[0],
            classified[1],
            picName
            )
        AddData(dataFile, data)
        logger.info(data)
        
        #works out necessary time to sleep
        counter += 1
        endTime = datetime.now(timezone.utc)
        timeTaken = endTime-timeNow
        if (timeTaken < timedelta(seconds=gapSecs)):
            sleep(gapSecs-timeTaken.total_seconds())
            timeNow = datetime.now(timezone.utc)

    except Exception as e:
        logger.error(f'{e.__class__.__name__}:{e}')
