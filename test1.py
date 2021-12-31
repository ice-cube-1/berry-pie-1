# This is the structure of the code for the experiment detecting wether
# something is land, sea or sky. It works correctly in its current state
# on a pi 4 running Flight OS (the operating system on the astro pi),
# however I didn't have a camera attached, which is why some is commented
# out (otherwise it would have had an error).
# Where to add code:
# - Emilia - the function capture is where it takes the photo, save it to
#   "picfile" and it should work fine
# - Izzy - Classification mock is for the AI bit, it takes in the file
#    where the picture is (called picName) and returns "classification"
#    a number between 0 and 2. Currently this number is generated randomly,
#    but it will be changed.
# - General note - there are a few sleeps, please delete them as they are
#    just to simulate how long the functions that you are writing might
#    take.
# - Also - there is no way this will run without errors on codingrooms,
#    when we zoom again I will run it on the pi but please don't edit the
#    code to fix syntax errors on codingrooms, because they aren't actual
#    errors, the importing is just weird.
#
# - Alice


from orbit import ISS
from pathlib import Path
from numpy import random  # placeholder
from datetime import datetime, timedelta, timezone
from picamera import PiCamera #unused, but will be
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
    # after placeholder removed the line below needs to be 
    # jpg instead of txt
    # takes a photo
    picName = "IMG"+str(counter).zfill(3)+".txt"
    picFile = baseFolder/picName
    captureMock(picFile)
    return(picName)


def captureMock(picFile):
    # captures the photo
    # this takes the photos, called picFile. placeholder below:
    # sleep will be removed, but it is there as a placeholder
    with open(picFile, "w") as f:
        f.write(str(counter))
    sleep(1)


def classificationMock(picName):
    # This is the AI bit. For now so that the rest of the code works,
    # There is a random number generator, obviously will be deleted.
    # The way it currently works is that one of 0,1,2 is
    # land, sea and sky, but this can be changed.
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

# set up camera (uncomment in real thing)
#PiCamera.resolution = (1296,972)

# nearly 3hr loop

start = datetime.now(timezone.utc)
timeNow = datetime.now(timezone.utc)

counter = 0
#below should be 30, but boring to test
gapSecs = 4

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
        #the print statements are unnessessary but useful for testing
        print("this took", timeTaken.total_seconds(), "secs", data)
        if (timeTaken > timedelta(seconds=gapSecs)):
            print("this overran")
        else:
            sleep(gapSecs-timeTaken.total_seconds())
        timeNow = datetime.now(timezone.utc)

    except Exception as e:
        logger.error(f'{e.__class__.__name__}:{e}')
