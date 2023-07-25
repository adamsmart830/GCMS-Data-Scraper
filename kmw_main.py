from collections import UserList
import pandas as pd
import numpy as np
import glob
import csv

import sample as s
import kmw_A as A
import kmw_B as B
import kmw_C as C

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
                if(lineCt > 4):
                    if(row[12] != ""):
                        sample = s.Sample(row[10], fileName, row[1])
                        #list = [fileName, row[1], row[10]]
                        if(dict.get(row[12]) == None):
                            dict[row[12]] = []
                        dict[row[12]].append(sample)
                        sample_array.append(sample)
                    else:
                        sample = s.Sample("Unknown CAS", fileName, row[1])
                lineCt+=1
###################################################################


#Sort Dicitonary by length of value array
def kSort(dict, keySort):         
    keySort = [k for k, v in sorted(dict.items(), key=lambda item: len(item[1]))]
    return keySort.reverse()


def printSampleArray(sample_array):
    for sample in sample_array:
        print("Sample Name: " + sample.sn + "\tRetention Time", str(sample.rt) + "\tProposed Compound:" + sample.pc )


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
        A.kmw_A(dict, keySort)
    elif(ui == 'b'):
        B.kmw_B(dict, keySort, sample_array)
    elif(ui == 'c'):
        C.kmw_C(sample_array)
    else:
        A.kmw_A(dict, keySort)
        B.kmw_B(dict, keySort, sample_array)
    
    #printSampleArray(sample_array)


if __name__ == "__main__":
    main()

