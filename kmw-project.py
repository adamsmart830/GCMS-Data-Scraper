import pandas as pd
import glob
import csv
from collections import UserList


#Class to hold information regarding a specific peak
class Sample:
    def __init__(self, _pc, _sn, _rt):
        self.pc = _pc
        self.sn = _sn
        self.rt = _rt

    def getPC(self):
        return self.pc

    def getSN(self):
        return self.sn
    
    def getRT(self):
        return self.rt
    

#Path to data files
path = './kmw-samples'
all_files = glob.glob(path + "/*.csv")

dict = {}

#Data scrape section
##################################################################
for files in all_files:
    with open(files, 'r', encoding = "ISO-8859-1") as file:
        csvreader = csv.reader(file)
        lineCt = 0
        fileName = ""
        for row in csvreader:
            if(lineCt == 2):
                fileName = row[0][9:20]
            if(lineCt > 4 and row[12] != ""):
                sample = Sample(row[10], fileName, row[1])
                #list = [fileName, row[1], row[10]]
                if(dict.get(row[12]) == None):
                    dict[row[12]] = []
                dict[row[12]].append(sample)
            lineCt+=1
###################################################################


#Sort Dicitonary by length of value array              
keySort = [k for k, v in sorted(dict.items(), key=lambda item: len(item[1]))]
keySort.reverse()


#print(keySort)


row_list = [["CAS ID", "Proposed Compound", "Found In Sample:", "At Retention Time"]]

for key in keySort:
    list_val = [key, "", "", ""]
    row_list.append(list_val) 

    for smpl in dict[key]:
        list_val = ['', smpl.pc, smpl.sn, smpl.rt]
        row_list.append(list_val)

with open('kmw-data-scrape.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)

file.close()

# Reading the csv file
df_new = pd.read_csv('kmw-data-scrape.csv')
 
# saving xlsx file
GFG = pd.ExcelWriter('kmw-data-scrape.xlsx')
df_new.to_excel(GFG, index=False)
 
GFG._save()

#print(row_list)

    

    