# -*- coding: utf-8 -*-

# This program will make a single output of Group Cohesion Scores
# from individual raw scores, downloaded from redcap. 

#Author: Sarah Hennessy, 2019

import os
import sys
import csv
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

def score(log, outpath):
    domain = 'MUSIC' #This is one of the following, always all caps:
                # COGNITIVE, SOCIOEMO, MUSIC, MOTOR, DEMO, OTHER
    #what is the outfile called?
    
    
    outfilename = outpath + "/groupcohesion.csv"
    
    exists = os.path.isfile(outfilename)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return

            
    
    data = pd.read_csv(log, header = "infer", skip_blank_lines = True, engine = "python")
    
#create a new dataframe 

    colnames = ['record_id','redcap_event_name','groupcohesion'] #make columns
    newdf = pd.DataFrame(columns = colnames) #create df 
    newdf['record_id'] = data['record_id'] #copy in record id


    if 'redcap_event_name' in data.columns:
        newdf['redcap_event_name'] = data['redcap_event_name']
    else:
        newdf['redcap_event_name'] = 'Year7'

    newdf['group'] = data['group']



#this loop adds up the total score and puts it in a row

    for index, row in data.iterrows():
        if row.group_cohesion_1 != "NaN":
            totalscore = row.group_cohesion_1 + row.group_cohesion_2 + row.group_cohesion_3 + row.group_cohesion_4 + row.group_cohesion_5 + row.group_cohesion_6 + row.group_cohesion_7 + row.group_cohesion_8 + row.group_cohesion_9
            newdf['groupcohesion'][index] =totalscore



#print to a new csv 
    newdf.to_csv(outfilename,index =False)

    print('congrats! you are now done with GROUP COHESION scoring.')


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    try: 
        score(*sys.argv[1:])
    except: 
        print("you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")
