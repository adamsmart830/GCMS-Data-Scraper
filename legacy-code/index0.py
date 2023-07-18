import pandas as pd
import glob
import csv
from collections import UserList


path = './kmw-samples'
all_files = glob.glob(path + "/*.csv")


dict = {}


def printNestedLists(li):
    for item in li:
        print("ok")



for files in all_files:
    with open(files, 'r', encoding = "ISO-8859-1") as file:
        csvreader = csv.reader(file)
        lineCt = 0
        fileName = ""
        for row in csvreader:
            if(lineCt == 2):
                fileName = row[0][9:20]
            if(lineCt > 4 and row[12] != ""):
                list = [fileName, row[1], row[10]]
                if(dict.get(row[12]) == None):
                    dict[row[12]] = []
                    dict[row[12]].append(list)
                else:
                    dict[row[12]].append(list)    

                
            lineCt+=1


dict = [k for k, v in sorted(dict.items(), key=lambda item: len(item[1]))]
print(dict)
row_list = [["CAS ID", "Sample Name", "Found In", "At Retention Time"]]


for key, values in dict.items():
    list_val = [key, "", "", ""]
    row_list.append(list_val)
    #print(key + ":")
    for val in values:
        list_val = ['', val[2], val[0], val[1]]
        row_list.append(list_val)
        #print("\t" + val[2] + "found in sample " + val[0] + " at retention time " + val[1])
        #print("\tFound in sample:" + val[0] + " at retention time:" + val[1] )

with open('new_csv.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)

file.close()

# Reading the csv file
df_new = pd.read_csv('new_csv.csv')
 
# saving xlsx file
GFG = pd.ExcelWriter('kmw-data-scrape.xlsx')
df_new.to_excel(GFG, index=False)
 
GFG._save()

#print(row_list)