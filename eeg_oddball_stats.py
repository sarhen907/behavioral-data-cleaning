# EEG txt export to excel for ERP data

# Choir study
# Oddball Task

#Sarah Hennessy
# March 27, 2020

import os
import sys
import csv
import pandas as pd
import numpy as np
import glob


def score(log, outpath):


    all_files = glob.glob(log + '/*'); #combining all files into this folder (VISIT 1)

    #what is the outfile called?
    outfilename = outpath + "/oddball_eegstats.csv"

    exists = os.path.isfile(outfilename)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return

    colnames = ['ID','time','group','variable', 'component', 'electrode', 'bin', 'value'] #make columns
    newdf = pd.DataFrame(columns = colnames)



    for filename in all_files:
        print(filename)
        data = pd.read_csv(filename, sep = "\t", skipinitialspace=True)

        #print(data.columns)

        if "visit1" in filename:
            time = 'pre'
        elif "visit2" in filename:
            time = 'mid'
        elif "visit3" in filename:
            time = 'post'

        print(time)

        if "choir" in filename:
            group = "choir"
        elif "control" in filename:
            group  = "control"


        component = "P3"



        if "lat" in filename:
            variable = "latency"
        elif "amp" in filename:
            variable = "amplitude"


        for index, row in data.iterrows():


            myid = row.ERPset[:4]


            if row.bini == 1:
                bin = "standard"
            elif row.bini == 3:
                bin = "oddball"
            elif row.bini == 5:
                bin = "distractor"

            electrode = data['chlabel'][index]


            value = data['value'][index]

            newdf = newdf.append({'ID': myid, 'time': time, 'group': group, 'component': component, 'variable': variable, 'bin': bin, 'electrode': electrode, 'value': value},ignore_index=True)


    newdf.to_csv(outfilename,index =False)
    print('congrats! you are now done with eeg oddball from txt to csv scoring.')

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    try:
        score(*sys.argv[1:])
    except:
        print("you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")
