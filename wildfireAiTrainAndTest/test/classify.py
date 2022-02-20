# imports
import csv
from PIL import Image
from pathlib import Path
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file
from os import listdir

# initalise + get AI name
AIName = input("AIname")
modelName = AIName+".tflite"
labelFileName = AIName+".txt"
script_dir = Path(__file__).parent.resolve()
model_file = script_dir/modelName
data_dir = script_dir/"data"
label_file = data_dir/labelFileName
interpreter = make_interpreter(f"{model_file}")
interpreter.allocate_tensors()

# creates CSV
def createCSV(dataFile):
    with open(dataFile,"w") as f:
        writer = csv.writer(f)
        header = ("classification","imageName")
        writer.writerow(header)

# adds data to CSV
def addData(data, dataFile):
    with open(dataFile,"a") as f:
        writer = csv.writer(f)
        writer.writerow(data)

# classifies an entire class
def classifyClass(className):
    csv_filename = className+".csv"
    csv_file = script_dir/csv_filename
    createCSV(csv_file)
    files = listdir(data_dir/className)
    for i in range(len(files)):
        picName = data_dir/className/files[i]
        data = classifyImage(picName),files[i]
        addData(data, csv_file)

# classifies a single image
def classifyImage(picName):
    size = common.input_size(interpreter)
    image = Image.open(picName).convert("RGB").resize(size, Image.ANTIALIAS)
    common.set_input(interpreter, image)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)
    labels = read_label_file(label_file)
    for c in classes:
        return(f'{labels.get(c.id, c.id)}')

# init
classNames = listdir(data_dir)
for i in range(len(classNames)):
    classifyClass(classNames[i])