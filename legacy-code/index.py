class Sample:
    def __init__(self, _sn,_rt):
        self.sn = _sn
        self.rt = _rt

import csv



Dict = {}

with open('./kmw-samples/kmw1-10-2.csv', 'r') as file:
    csvreader = csv.reader(file)
    lineCt = 0
    fileName = ""
    for row in csvreader:
        if(lineCt == 2):
            fileName = row[0][9:20]
            #print(row[0])
        if(lineCt > 4):
            s = Sample(fileName, row[1])
            Dict[row[12]] = fileName, row[1]
            Dict[row[12]] = fileName, row[1]

        lineCt+=1



print(Dict.items())
print(fileName)