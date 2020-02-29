# -*- coding: utf-8 -*-

# This program will make a single output of MindsetAssessment Scores 
#from individual raw scores, downloaded from redcap.

#Author: Sarah Hennessy, 2019


import os
import sys
import csv
import pandas as pd
import numpy as np


import warnings
warnings.filterwarnings("ignore")


def score(log, outpath):

#what is the outfile called?
    domain = 'SOCIOEMO' #This is one of the following, always all caps:
                # COGNITIVE, SOCIOEMO, MUSIC, MOTOR, DEMO, OTHER

    outfilename = outpath + "/mindset.csv"
    exists = os.path.isfile(outfilename)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return

    data = pd.read_csv(log, header = "infer", skip_blank_lines = True, engine = "python")

#create a new dataframe 

    colnames = ['record_id','redcap_event_name','mindset_score', 'mindset_group'] #make columns
    newdf = pd.DataFrame(columns = colnames) #create df 
    newdf['record_id'] = data['record_id'] #copy in record id

    if 'redcap_event_name' in data.columns:
        newdf['redcap_event_name'] = data['redcap_event_name']
    else:
        newdf['redcap_event_name'] = 'Year7'
    
    newdf['group'] = data['group']


#this function will backwards score what needs to be backwards scored

    def backwards_score(score): 
        global backscore #this makes this variable usable outside of this function
        if score == 1:
            backscore = 6
        elif score == 2:
            backscore = 5
        elif score == 3:
            backscore = 4
        elif score == 4:
            backscore = 3
        elif score == 5:
            backscore = 2
        elif score == 6:
            backscore = 1
    

#this loop adds up the total score and puts it in a row


    for index, row in data.iterrows():
        if row.mindset_assesment_profile_complete == 2:
            
            #first, compute the total score
            
            negativelist = []
            negative = []
            positive = []
            
            positive = row.map1 + row.map3 + row.map5 + row.map7
            backlist = [row.map2, row.map4, row.map6, row.map8]
            for j in backlist: 
                backwards_score(j) #call my above-defined function
                negativelist = negativelist + [backscore] #keep adding to the list 
                negative = sum(negativelist) #add scores from that list
            totalscore = negative + positive #add lists together
            
            #add it to the dataframe
            newdf['mindset_score'][index] =totalscore
            
            #second, compute the mindset group
            
            if totalscore <= 12 and totalscore >= 8:
                group = 'F5'
            elif totalscore <= 16 and totalscore >= 13:
                group = 'F4'
            elif totalscore <= 20 and totalscore >= 17:
                group = 'F3'
            elif totalscore <= 24 and totalscore >= 21:
                group = 'F2'
            elif totalscore <= 28 and totalscore >= 25:
                group = 'F1'
            elif totalscore <= 32 and totalscore >= 29:
                group = 'G1'
            elif totalscore <= 36 and totalscore >= 33:
                group = 'G2'
            elif totalscore <= 40 and totalscore >= 37:
                group = 'G3'
            elif totalscore <= 44 and totalscore >= 41:
                group = 'G4'
            elif totalscore <= 48 and totalscore >= 45:
                group = 'G5'
            else:
                group = 'NaN'
                
            #add it to the dataframe
            newdf['mindset_group'][index] = group
        else:
            newdf['mindset_group'][index] = ''
            newdf['mindset_score'][index] = ''
            
            
            
        

    #print to a new csv 
    newdf.to_csv(outfilename,index =False)
    
    print('congrats! you are now done with MINDSET ASSESSMENT scoring.')


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    try: 
        score(*sys.argv[1:])
    except: 
        print("you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")

