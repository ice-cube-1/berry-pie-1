from orbit import ISS
from pathlib import Path
from numpy import random  # placeholder
from datetime import datetime, timedelta, timezone
from picamera import PiCamera
from logzero import logger, logfile
from time import sleep
import csv


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
        "Classification", "ImageName")
        writer.writerow(header)


def AddData(dataFile, data):
    #adds data to the CSV file
    with open(dataFile, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def takePhoto(counter):
    picName = "IMG"+str(counter).zfill(3)+".jpg"
    picFile = f"{baseFolder}/{picName}"
    camera.capture(picFile)
    return(picName)


def classificationMock(picName):
    # This is the AI bit. For now so that the rest of the code works,
    # There is a random number generator, obviously will be deleted.
    # The way it currently works is that one of 0,1,2 is
    # land, sea and sky, but this will be changed.
    classification = random.randint(0, 3)
    sleep(2)
    return classification

# set up CSV
baseFolder = Path(__file__).parent.resolve()
dataFile = baseFolder/"data.csv"
CreateCSV(dataFile)

# set up logfile, which collects the data in a harder to understand
# format but will stay there if the program is restarted and holds
# errors.
logfile(baseFolder/"events.log")

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
        classifation = classificationMock(picName)
        data = (
            str(counter).zfill(3),
            timeNow.isoformat(), 
            loc[0], 
            loc[1], 
            classifation, 
            picName
            )
        AddData(dataFile, data)
        logger.info(data)
        
        #works out necessary time to sleep
        counter += 1
        endTime = datetime.now(timezone.utc)
        timeTaken = endTime-timeNow
        if (timeTaken > timedelta(seconds=gapSecs)):
            print("this overran")
        else:
            sleep(gapSecs-timeTaken.total_seconds())
        timeNow = datetime.now(timezone.utc)

    except Exception as e:
        logger.error(f'{e.__class__.__name__}:{e}')
