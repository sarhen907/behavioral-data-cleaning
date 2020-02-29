#This program will aggregate all other scripts, running them at one time. 
#It will keep the outputs from each individual script, 
#while also creating a single "All Data" output. 

#Author: Sarah Hennessy, 2019

import os
import sys
import csv
import pandas as pd
import numpy as np
import glob

study = input("What study would you like to score? (1) = SCHOOL, (2) = LONGITUDINAL ")

if eval(study) == 1:
    print('you selected SCHOOL. Great choice.')
elif eval(study) == 2:
    print('you selected LONGITUDINAL. Great selection!') 

rawdata = input("Where is your raw data coming from? ")
rawdata = rawdata[:-1]

going = input("Where would you like your output to go? ")
going = going[:-1]



allout = going + "/ALLDATA.csv"

exists1 = os.path.isfile(allout)
if exists1:
    overwrite = input('stop! An ALLDATA file already exists! are you sure you want to overwrite? y or n: ')
    if overwrite == 'n':
        print('ok. quitting now.')
        exit
    


print('Beginning scoring...')
#run the tasks in common                     
import BASC_parent
print("starting BASC_parent...")
BASC_parent.score(rawdata,going)

import MindsetAssessment
print("starting mindset...")
MindsetAssessment.score(rawdata,going)


if eval(study) == 1:
    
    
    print('blah')
    #1. run the scripts (Different)
    
   # import BASC_parent
    #print("starting BASC_parent...")
   # BASC_parent.score(rawdata,going)
    
 
elif eval(study) == 2:
    #1. run the different scripts 
    
    import RAVLT
    print("starting RAVLT...")
    RAVLT.score(rawdata,going)
    
    import GroupCohesion
    print("starting Group Cohesion...")
    GroupCohesion.score(rawdata,going)
    

else: 
    print("That is not a valid study! please try again.")
    
    
    
#2. Create an all data sheet 
print("Beginning aggregation for all data...")    


all_files = glob.glob(going+ "/*.csv")


if (going + '/ALLDATA.csv') in all_files:
    all_files.remove(going + '/ALLDATA.csv')
    

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
  
frame2 = pd.merge(li[1], li[2], on = ["record_id", "group", "redcap_event_name"])

for k in range(2,len(li)):
    frame = pd.merge(frame2, li[k], on = ["record_id", "group", "redcap_event_name"])

     
cols = frame.columns.tolist()
cols.insert(0,cols.pop(cols.index('group')))
cols.insert(0,cols.pop(cols.index('redcap_event_name')))
cols.insert(0,cols.pop(cols.index('record_id')))
frame = frame.reindex(columns= cols)

frame.to_csv(allout,index =False)
    

print("\n\nFull scoring protocol complete. \nPlease upload all data spreadsheet to RedCap.\n Goodbye!")
    
    
    
    


