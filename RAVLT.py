
# coding: utf-8

# This program will make a single output of RAVLT Scores from individual raw scores, downloaded from redcap.

# Author: Sarah Hennessy, 2019


import os
import sys
import csv
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

def score(log, outpath):
    domain = 'COGNITIVE' #This is one of the following, always all caps:
                # COGNITIVE, SOCIOEMO, MUSIC, MOTOR, DEMO, OTHER
    #what is the outfile called?
    outfilename = outpath + "/RAVLT.csv"
    exists = os.path.isfile(outfilename)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return
    
    data = pd.read_csv(log, header = "infer", skip_blank_lines = True, engine = "python")
    
    #create a new dataframe 
    
    colnames = ['record_id','redcap_event_name','group','ravlt_best_learning', 'ravlt_learning_rate', 'ravlt_total_learning','ravlt_delayed_recall', 'ravlt_retro_interference', 'ravlt_forgetting_rate', 'ravlt_recognition_hits', 'ravlt_recognition_fa', 'ravlt_recognition'] #make columns
    newdf = pd.DataFrame(columns = colnames) #create df 
    newdf['record_id'] = data['record_id'] #copy in record id
    
    if 'redcap_event_name' in data.columns:
        newdf['redcap_event_name'] = data['redcap_event_name']
    else:
        newdf['redcap_event_name'] = 'Year7'
        
    
    newdf['group'] = data['group']
    
    
    
    for index, row in data.iterrows():
        if row.ravlt_complete == 2:
            
            #RECALL BLOCK
            
            #sums of individual recalls
            r1 = row.filter(regex = 'ravlt_a1_raw___[0-9]+').sum(axis=0)
            r2 = row.filter(regex = 'ravlt_a2_raw___[0-9]+').sum(axis=0)
            r3 = row.filter(regex = 'ravlt_a3_raw___[0-9]+').sum(axis=0)
            r4 = row.filter(regex = 'ravlt_a4_raw___[0-9]+').sum(axis=0)
            r5 = row.filter(regex = 'ravlt_a5_raw___[0-9]+').sum(axis=0)
            r6 = row.filter(regex = 'ravlt_a6_raw___[0-9]+').sum(axis=0)
            r7 = row.filter(regex = 'ravlt_a7_raw___[0-9]+').sum(axis=0)
            
            rlist = [r1,r2,r3,r4,r5]
            #print(rlist)
            
            
            #BESTLEARN
            bestlearn = r5
            newdf['ravlt_best_learning'][index] = bestlearn
            
            #LEARNING RATE
            learnrate = (r5-r1)
            newdf['ravlt_learning_rate'][index] = learnrate
            
            #TOTAL LEARN
            totallearn = sum(rlist)
            newdf['ravlt_total_learning'][index] = totallearn
            
            #DELAYED RECALL
            delayedrecall = r6
            newdf['ravlt_delayed_recall'][index] = delayedrecall
            
            #RETROACTIVE INTERFERENCE
            retro = (r5-r6)
            newdf['ravlt_retro_interference'][index] = retro
            
            #FORGETTING RATE
            forget = (r5-r7)
            newdf['ravlt_forgetting_rate'][index] = forget
            
            #RECOGNITION BLOCK
            
            recall_cols = row.filter(regex = 'ravlt_rec_')
            
            #list1 
            recall_list1 = recall_cols.filter(regex = '1')
            list1hit_list = []
            for j in range(1,(len(recall_list1))):
                if recall_list1[j] == 1:
                    list1hit = 1
                elif recall_list1[j] == 0 or recall_list1[j] == 2:
                    list1hit = 0
    
            list1hit_list = list1hit_list + [list1hit]        
            
            hits1 = sum(list1hit_list)
            
            #list2
            recall_list2 = recall_cols.filter(regex = '2')
            list2hit_list = []
            for j in range(1,(len(recall_list2))):
                if recall_list2[j] == 2:
                    list2hit = 1
                elif recall_list2[j] == 0 or recall_list2[j] == 1:
                    list2hit = 0
    
            list2hit_list = list2hit_list + [list2hit]        
            
            hits2 = sum(list2hit_list)
                
            #list0
            recall_list0 = recall_cols.filter(regex = '0')
            list0fa_list = []
            for j in range(1,(len(recall_list0))):
                if recall_list0[j] == 0:
                    fa = 0
                elif recall_list0[j] == 2 or recall_list0[j] == 1:
                    fa = 1
    
            list0fa_list = list0fa_list + [fa]        
    
    
            fa_sum = sum(list0fa_list)
            totalhits = (hits1 + hits2)
            falsealarms = fa_sum
            recog = (totalhits-falsealarms)
            
            newdf['ravlt_recognition_hits'][index] = totalhits
            newdf['ravlt_recognition_fa'][index] =falsealarms
                
            newdf['ravlt_recognition'][index] = recog
        else:
            newdf['ravlt_best_learning'][index] = ''
            newdf['ravlt_learning_rate'][index]=''
            newdf['ravlt_total_learning'][index] =''
            newdf['ravlt_delayed_recall'][index] = ''
            newdf['ravlt_retro_interference'][index] =''
            newdf['ravlt_forgetting_rate'][index] =''
            newdf['ravlt_recognition_hits'][index] = ''
            newdf['ravlt_recognition_fa'][index] = ''
            newdf['ravlt_recognition'][index] = ''
    
    #print to a new csv 
    newdf.to_csv(outfilename,index =False)
    
    
    print('congrats! you are now done with RAVLT scoring.')


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    try: 
        score(*sys.argv[1:])
    except: 
        print("you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")






