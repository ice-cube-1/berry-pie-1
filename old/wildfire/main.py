from orbit import ISS
from pathlib import Path
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
    # gets the latitude andlongitude of the ISS
    location = ISS.coordinates()
    latitude = location.latitude.degrees
    longitude = location.longitude.degrees
    return(latitude, longitude)


def CreateCSV(dataFile):
    # creates a CSV file
    with open(dataFile, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter","Date/Time", "Latitude", "Longitude",
        "Classification", "ImageName")
        writer.writerow(header)


def AddData(dataFile, data):
    # adds data to the CSV file
    with open(dataFile, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def takePhoto(counter):
    # takes the photo
    picName = "IMG"+str(counter).zfill(3)+".jpg"
    picFile = f"{script_dir}/data/{picName}"
    camera.capture(picFile)
    return(picFile)


def classification(picName):
    # classifies the photo
    image_file = picName
    image = Image.open(image_file).convert('RGB').resize(size1, Image.ANTIALIAS)
    common.set_input(interpreter,image)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)
    labels = read_label_file(label_file)
    for c in classes:
        return(labels.get(c.id, c.id))


# initialize the AI
script_dir = Path(__file__).parent.resolve()
model_file = script_dir/'wildfire-vs-nonwildfire.tflite'
label_file = script_dir/'wildfire-vs-nonwildfire.txt'
interpreter = make_interpreter(f"{model_file}")
interpreter.allocate_tensors()
size1 = common.input_size(interpreter)


# set up CSV
dataFile = script_dir/"data.csv"
CreateCSV(dataFile)

# set up logfile, which collects the data in a harder to understand
# format but will stay there if the program is restarted and holds
# errors.
logfile(script_dir/"events.log")

# set up camera
camera = PiCamera()

# sets the clock for the experiment
start = datetime.now(timezone.utc)
timeNow = datetime.now(timezone.utc)
counter = 0
gapSecs = 30

while (timeNow < start+timedelta(minutes=178)):
    try:
        # add the data
        loc = getLocation()
        picName = takePhoto(counter)
        classified = classification(picName)
        data = (
            str(counter).zfill(3),
            timeNow.isoformat(), 
            loc[0], 
            loc[1], 
            classified,
            picName
            )
        AddData(dataFile, data)
        logger.info(data)
        
        # works out necessary time to sleep
        counter += 1
        endTime = datetime.now(timezone.utc)
        timeTaken = endTime-timeNow
        if (timeTaken < timedelta(seconds=gapSecs)):
            sleep(gapSecs-timeTaken.total_seconds())
            timeNow = datetime.now(timezone.utc)

    # makes sure an error does not stop the whole code from running.
    except Exception as e:
        logger.error(f'{e.__class__.__name__}:{e}')
