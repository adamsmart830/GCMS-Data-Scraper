import kmw_main as im
# NOTE: Any tag with the im. attatched solely is for import support


def kmw_A(dict, keySort):
    row_list = [["CAS ID", "Proposed Compound", "Found In Sample:", "At Retention Time"]]

    for key in keySort:
        list_val = [key, "", "", ""]
        row_list.append(list_val) 

        for smpl in dict[key]:
            list_val = ['', smpl.pc, smpl.sn, smpl.rt]
            row_list.append(list_val)

    with open('../output/kmw-data-scrape-A.csv', 'w', newline='') as file:
        writer = im.csv.writer(file)
        writer.writerows(row_list)

    file.close()

    # Reading the csv file
    df_new = im.pd.read_csv('../output/kmw-data-scrape-A.csv')
    
    # saving xlsx file
    GFG = im.pd.ExcelWriter('../output/kmw-data-scrape-A.xlsx')
    df_new.to_excel(GFG, index=False)
    
    GFG._save()

    #print(row_list)  print("Hello World")




    