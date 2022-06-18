from pathlib import Path
import csv
scriptDir = Path(__file__).parent.resolve()

def importCSV(CSV):
    csvAsList=[]
    with open(scriptDir/CSV, mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            classified=line[1]
            actual=line[2]
            csvAsList.append([classified,actual])
        return csvAsList

def overallAccuracy(data):
    correct=0
    for i in range(len(data)):
        if data[i][0] == data[i][1]:
            correct+=1
    return (correct/len(data))*100

def accuracy(actual,data):
    classified=[0,0,0]
    for i in range(len(data)):
        if data[i][1]==actual:
            if data[i][0]=="random":
                classified[0]+=1
            elif data[i][0]=="sea":
                classified[1]+=1
            else:
                classified[2]+=1
    total=classified[0]+classified[1]+classified[2]
    return str(actual)+str((total/len(data)*100))+":\nRandom:"+str((classified[0]/total)*100)+"\nSea:"+str((classified[1]/total)*100)+"\nLand:"+str((classified[2]/total)*100)
            

data = importCSV("data.csv")
print(overallAccuracy(data))
print(accuracy("land",data))
print(accuracy("sea",data))
print(accuracy("random",data))