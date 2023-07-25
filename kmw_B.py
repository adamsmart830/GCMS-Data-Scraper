import kmw_main as im
# NOTE: Any tag with the im. attatched solely is for import support

def kmw_B(dict, keySort, sample_array):
    rt_dict = {}
    getSTDevDict(dict, keySort, rt_dict)
    new_rt_dict = {}
    parseData(rt_dict, new_rt_dict, sample_array)
    
    outputB(rt_dict, new_rt_dict)


def getSTDevDict(dict, keySort, rt_dict):
    for key in keySort:
        temp = 0
        ct = 0
        retention_list = []
        for sample in dict[key]:
            retention_list.append(sample.rt)
            temp += sample.rt
            ct += 1

        avg_rt = round((temp / ct), 3)
        rt_dict[avg_rt] = 0.01#round(max(min(np.std(retention_list), 0.1), 0.01), 3)
        #print(rt_dict)


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



def outputB(rt_dict, new_rt_dict):
    rt_dict = dict(sorted(rt_dict.items(), key=lambda item:item[0]))
    keysList = list(new_rt_dict.keys())
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
        writer = im.csv.writer(file)
        writer.writerows(row_list)

    file.close()

    # Reading the csv file
    df_new = im.pd.read_csv('../output/kmw-data-scrape-B.csv')
    
    # saving xlsx file
    GFG = im.pd.ExcelWriter('../output/kmw-data-scrape-B.xlsx')
    df_new.to_excel(GFG, index=False)
    
    GFG._save()

    #print(row_list)  print("Hello World")