import pandas as pd
import glob
import csv
from collections import UserList


#Class to hold information regarding a specific peak
#################################################################
class Sample:
    def __init__(self, _pc, _sn, _rt):
        self.pc = _pc
        self.sn = _sn
        self.rt = float(_rt)

    def getPC(self):
        return self.pc

    def getSN(self):
        return self.sn
    
    def getRT(self):
        return self.rt
#################################################################



#Data scrape section
##################################################################
def dataScrape(all_files, dict, sample_array):
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
                    sample_array.append(sample)
                lineCt+=1
###################################################################


#Sort Dicitonary by length of value array
def kSort(dict, keySort):         
    keySort = [k for k, v in sorted(dict.items(), key=lambda item: len(item[1]))]
    return keySort.reverse()


#print(keySort)


def kmw_A(dict, keySort):
    row_list = [["CAS ID", "Proposed Compound", "Found In Sample:", "At Retention Time"]]

    for key in keySort:
        list_val = [key, "", "", ""]
        row_list.append(list_val) 

        for smpl in dict[key]:
            list_val = ['', smpl.pc, smpl.sn, smpl.rt]
            row_list.append(list_val)

    with open('../output/kmw-data-scrape-A.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)

    file.close()

    # Reading the csv file
    df_new = pd.read_csv('../output/kmw-data-scrape-A.csv')
    
    # saving xlsx file
    GFG = pd.ExcelWriter('../output/kmw-data-scrape-A.xlsx')
    df_new.to_excel(GFG, index=False)
    
    GFG._save()

    #print(row_list)  print("Hello World")

def kmw_B(dict, keySort, sample_array):
    rt_dict = {}
    getSTDevDict(dict, keySort, rt_dict)
    new_rt_dict = {}
    parseData(rt_dict, new_rt_dict, sample_array)
    
    outputB(rt_dict, new_rt_dict)

def outputB(rt_dict, new_rt_dict):
    rt_dict = dict(sorted(rt_dict.items(), key=lambda item:item[0]))
    keysList = list(rt_dict.keys())
    row_list = [["Retention Time", "Standard Deviation", "Proposed Compound", "Sample", "Actual Retention Time"]]
    
    for key in keysList:
        list_val = [key, rt_dict[key], "", "", ""]
        row_list.append(list_val)
        for sample in new_rt_dict[key]:
            list_val = ["", "", sample.pc, sample.sn, sample.rt]
            row_list.append(list_val)
        list_val = ["", "","","",""]
        row_list.append(list_val)
        
    with open('../output/kmw-data-scrape-B.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)

    file.close()

    # Reading the csv file
    df_new = pd.read_csv('../output/kmw-data-scrape-B.csv')
    
    # saving xlsx file
    GFG = pd.ExcelWriter('../output/kmw-data-scrape-B.xlsx')
    df_new.to_excel(GFG, index=False)
    
    GFG._save()

    #print(row_list)  print("Hello World")


def parseData(rt_dict, new_rt_dict, sample_array):
    rt_dict = dict(sorted(rt_dict.items(), key=lambda item:item[0]))
    keysList = list(rt_dict.keys())
    for key in keysList:
        stdev = rt_dict[key]
        for sample in sample_array:
            if((key + stdev) > sample.rt and (key - stdev) < sample.rt):
                if(new_rt_dict.get(key) == None):
                    new_rt_dict[key] = []
                new_rt_dict[key].append(sample)
        
    #print(new_rt_dict)


        



def getSTDevDict(dict, keySort, rt_dict):
    for key in keySort:
        ct = 0
        avg_rt = 0
        low = 0
        high = 0
        for sample in dict[key]:
            sample_rt = float(sample.rt)
            if ct == 0:
                low = sample_rt
                high = sample_rt
            else:
                if(low > sample_rt):
                    low = sample_rt
                if(high < sample_rt):
                    high = sample_rt
            avg_rt += sample_rt
            ct+=1
        avg_rt = avg_rt / ct
        abs_rt_h = abs(high - avg_rt)
        abs_rt_l = abs(low - avg_rt)
        std_dev = max(abs_rt_h, abs_rt_l, 0.01)
        rt_dict[avg_rt] = std_dev

    #print(rt_dict)


def main():
    
    # Path to data files
    path = '../kmw-samples'
    all_files = glob.glob(path + "/*.csv")
    dict = {}
    sample_array = []

    # Populate Dictionary
    dataScrape(all_files, dict, sample_array)

    # Sort Dict Keys
    keySort = [k for k, v in sorted(dict.items(), key=lambda item: len(item[1]))]
    keySort.reverse()

    # Grab User Input (ui)
    ui = input("Enter Program (A/B/C):")
    ui = ui.lower()

    # Program selection
    if(ui == 'a'):
        kmw_A(dict, keySort)
    elif(ui == 'b'):
        kmw_B(dict, keySort, sample_array)
    else:
        kmw_A(dict, keySort)
        kmw_B(dict, keySort, sample_array)








if __name__ == "__main__":
    main()


    