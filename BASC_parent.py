
# coding: utf-8

# This program will make a single output of BASC Parent Scores from individual raw scores, downloaded from redcap.
# 
# Author: Sarah Hennessy, 2019

# In[443]:


import os
import sys
import csv
import pandas as pd
import numpy as np


# In[444]:

import warnings
warnings.filterwarnings("ignore")

def score(log, outpath): 



#what is the outfile called?
    domain = 'SOCIOEMO' #This is one of the following, always all caps:
                # COGNITIVE, SOCIOEMO, MUSIC, MOTOR, DEMO, OTHER
    outfilename = outpath + "/BASC_parent.csv"
    exists = os.path.isfile(outfilename)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return

    data = pd.read_csv(log, header = "infer", skip_blank_lines = True, engine = "python")


    colnames = ['record_id','redcap_event_name','group', 'basc_parent_raw', 'basc_parent_daily_activities','basc_parent_adaptability','basc_parent_aggression','basc_parent_anxiety','basc_parent_attention_problems','basc_parent_depression','basc_parent_functional_communication','basc_parent_hyperactivity','basc_parent_leadership','basc_parent_social_skills','basc_parent_somatization','basc_parent_tscore','basc_parent_percentile']
    newdf = pd.DataFrame(columns = colnames) #create df 
    newdf['record_id'] = data['record_id'] #copy in record id

    if 'redcap_event_name' in data.columns:
        newdf['redcap_event_name'] = data['redcap_event_name']
    else:
        newdf['redcap_event_name'] = 'Year7'
    
    
    newdf['group'] = data['group']



# MAKE MATRICES FOR NORMS

#MID AGE T SCORES 

    mid_age_t = list(range(30,103))
    addins = [100, 96,92,88,84,81,77,73,69,65,61,57,53,49,45,41,37,33]
    mid_age_t = mid_age_t + addins
    mid_age_t.sort()


#MID AGE PERCENTILES 

    mid_age_p = list(range(1,100))
    mid_age_p = set(mid_age_p)
    deleteme = [85, 82, 80, 87, 79, 90] + list(range(75,78)) + [73, 70, 71] + list(range(66,69)) + list(range(62,65)) + list(range(59,61)) + list(range(56,58)) + list(range(51,55)) + list(range(47,50))+ list(range(43,46)) + list(range(39,42)) + list(range(35,38)) +  list(range(30,34)) +  list(range(27,29)) + list(range(24,26))+ list(range(18,23)) + list(range(16,19)) + [14, 12] + list(range(9,11)) + [7, 3]
    mid_age_p = mid_age_p - set(deleteme)
    addins = [99] * 34 + [98] *2 + [97] + [96]*2 + [92] + [86] +[78] + [65] + [50] +[34] +[19] + [8] + [2] +[1] *2 + [19]
    mid_age_p = addins + list(mid_age_p)
    mid_age_p.sort()


# LOW AGE T SCORES
    low_age_t = list(range(28,107))
    addins = [29,35,42,48,55,61,67,74,80,86,93,99]
    low_age_t = low_age_t + addins
    low_age_t.sort()


# LOW AGE PERCENTILES

    low_age_p = list(range(1,100))
    addins = [1]*5 + [5] +  [22] + [46] + [72, 86,94,96,97] + [98]*3 + [99]*34 
    deleteme = [4,6,8,11,13,15,16,17,19,20,21,23,24,25,27,28,30,31,33,34,35,37,38,39,40,42,43,44,45] + list(range(47,52)) + list(range(53,56)) + [57,58] + [60,61, 77,79,81,83,85, 87,88,] + list(range(63,65)) + [66,67]+ list(range(69,72))+ list(range(73,76))
    low_age_p = set(low_age_p)
    low_age_p = low_age_p - set(deleteme)
    low_age_p = addins + list(low_age_p)
    low_age_p.sort()


    normnames = ['mid_age_p','mid_age_t','low_age_p','low_age_t']
    norms = pd.DataFrame(columns = normnames)
    norms['mid_age_p'] = mid_age_p
    norms['mid_age_t']= mid_age_t
    norms['low_age_p']=low_age_p
    norms['low_age_t']= low_age_t

    def backwards_score(score): 
        global backscore #this makes this variable usable outside of this function
        if score == 3:
            backscore = 0
        elif score == 2:
            backscore = 1
        elif score == 1:
            backscore = 2
        elif score == 0:
            backscore = 3
   

#Create wrong-data frame

    manipdata = data.filter(regex = 'basic_parent_[0-9]')
    moremani = data.filter(regex = 'basc_parent_[0-9]+')
    manip = pd.DataFrame(manipdata)
    manip2 = pd.DataFrame(moremani)
    manip1 = pd.concat([manip,manip2], axis = 1)

    manip1['parent_basc_parent_form_complete'] = data['parent_basc_parent_form_complete']
    manip1['basc_age'] = data['basc_age']


    backlist_names = ['basic_parent_1', 'basic_parent_3','basic_parent_5', 'basic_parent_7', 'basic_parent_9', 'basic_parent_11', 'basic_parent_13', 'basic_parent_15','basic_parent_17', 'basic_parent_19', 'basc_parent_21', 'basc_parent_23', 'basc_parent_25', 'basc_parent_27', 'basc_parent_29']



#fix the wrong data set and make it the right data set

    for index, row in manip1.iterrows():
        backlist = [row.basic_parent_1, row.basic_parent_3, row.basic_parent_5, row.basic_parent_7, row.basic_parent_9, row.basic_parent_11, row.basic_parent_13, row.basic_parent_15,row.basic_parent_17, row.basic_parent_19, row.basc_parent_21, row.basc_parent_23, row.basc_parent_25, row.basc_parent_27, row.basc_parent_29]
    
        count = -1
        for j in backlist:  
            count = count + 1
            backwards_score(j)
            manip1[backlist_names[count]][index] = backscore
 
    
#use the right dataset as the reference for rest of script

    for index, row in manip1.iterrows():
    
        if row.parent_basc_parent_form_complete == 2:

    #RAW SCORES
    
            partialsum = row.filter(regex = 'basic_parent_[0-9]+').sum(axis=0)
            moresum = row.filter(regex = 'basc_parent_[0-9]+').sum(axis=0)
            totalsum = partialsum + moresum
    
            newdf['basc_parent_raw'][index] = totalsum
    
    #SUBSCALES
    
            activities = row.basic_parent_12 + row.basc_parent_30
            newdf['basc_parent_daily_activities'][index] = activities
    
            adapt = row.basic_parent_17 + row.basc_parent_28
            newdf['basc_parent_adaptability'][index] = adapt
    
            aggress = row.basic_parent_10 + row.basc_parent_26
            newdf['basc_parent_aggression'][index] = aggress
    
            anxiety = row.basic_parent_16 + row.basic_parent_11 +row.basc_parent_25
            newdf['basc_parent_anxiety'][index] = anxiety
    
            attn = row.basic_parent_1 + row.basic_parent_8  +row.basc_parent_22 +row.basc_parent_27
            newdf['basc_parent_attention_problems'][index] = attn
    
            dep = row.basic_parent_7 + row.basic_parent_13  +row.basc_parent_23 +row.basc_parent_29
            newdf['basc_parent_depression'][index] = dep
    
            com = row.basic_parent_3 + row.basic_parent_15
            newdf['basc_parent_functional_communication'][index] = com
    
            hyp = row.basic_parent_6 +row.basic_parent_20
            newdf['basc_parent_hyperactivity'][index] = hyp
    
            lead = row.basic_parent_9 +row.basic_parent_19
            newdf['basc_parent_leadership'][index] = lead
    
            soc = row.basic_parent_5 + row.basc_parent_24
            newdf['basc_parent_social_skills'][index] = soc
    
            soma = row.basic_parent_14 + row.basc_parent_21
            newdf['basc_parent_somatization'][index] = soma
        
     #STANDARD SCORES
        
            if row.basc_age >= 10:
        
                tscore = norms['mid_age_t'][totalsum]
                percent = norms['mid_age_p'][totalsum]
    
                newdf['basc_parent_tscore'][index]= tscore
                newdf['basc_parent_percentile'][index] = percent
            else:
                tscore = norms['low_age_t'][totalsum]
                percent = norms['low_age_p'][totalsum]
    
                newdf['basc_parent_tscore'][index]= tscore
                newdf['basc_parent_percentile'][index] = percent
            
    
        else: 
            newdf['basc_parent_raw'][index] = ''
            newdf['basc_parent_daily_activities'][index] = ''
            newdf['basc_parent_adaptability'][index] =''
            newdf['basc_parent_aggression'][index] =''
            newdf['basc_parent_anxiety'][index] =''
            newdf['basc_parent_attention_problems'][index] =''
            newdf['basc_parent_depression'][index] =''
            newdf['basc_parent_functional_communication'][index] =''
            newdf['basc_parent_hyperactivity'][index] =''
            newdf['basc_parent_tscore'][index]=''
            newdf['basc_parent_percentile'][index] =''
            newdf['basc_parent_somatization'][index] =''
            newdf['basc_parent_social_skills'][index] =''
            newdf['basc_parent_leadership'][index] = ''
        
        
    newdf.to_csv(outfilename,index =False)
    print('congrats! you are now done with BASC PARENT scoring.')




if __name__ == '__main__':
    # Map command line arguments to function arguments.
    try: 
        score(*sys.argv[1:])
    except: 
        print("you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")
    
    
    
    
    
    
    
    
    
  
    
    
    
    
    

