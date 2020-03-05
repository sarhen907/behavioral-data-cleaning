


# This script scores Singing Attitudes. Documentation can be found in Welch et al., 2014, "Singing and Social Inclusion".
# Last update: 1/30/20

#Author: Sarah Hennessy

import os
import sys
import csv
import pandas as pd
import numpy as np


def score(log, outpath):

    domain = 'MUSIC' #This is one of the following, always all caps:
                # COGNITIVE, SOCIOEMO, MUSIC, MOTOR, DEMO, OTHER


    #what is the outfile called?
    outfilename = outpath + "/singing_attitudes.csv"


    exists = os.path.isfile(outfilename)
    if exists:
        overwrite = input('stop! this file already exists! are you sure you want to overwrite? y or n: ')
        if overwrite == 'n':
            print('ok. quitting now.')
            return

    data = pd.read_csv(log, header = "infer", skip_blank_lines = True, engine = "python")



    colnames = ['record_id','redcap_event_name', 'group', 'enviro_school', 'enviro_home','enviro_informal','identity_self','identity_emotion','self_social'] #make columns


    newdf = pd.DataFrame(columns = colnames) #create df



    newdf['record_id'] = data['record_id'] #copy in record id





    if 'redcap_event_name' in data.columns:
        newdf['redcap_event_name'] = data['redcap_event_name']
    else:
        newdf['redcap_event_name'] = 'Year7'



    newdf['group'] = data['group']



    def backwards_score(score):
        global backscore #this makes this variable usable outside of this function
        if score == 1:
            backscore = 7
        elif score == 2:
            backscore = 6
        elif score == 3:
            backscore = 5
        elif score == 4:
            backscore = 4
        elif score == 5:
            backscore = 3
        elif score == 6:
            backscore = 2
        elif score == 7:
            backscore = 1

    print('i read a backwards function in')


    for index, row in data.iterrows():

        if row.singing_attitudes_complete == 2: #2 = complete

            negativelist = []

            #positive = row.map1 + row.map3 + row.map5 + row.map7
            backlist = [row.singatt_18, row.singatt_26 , row.singatt_31, row.singatt_36, row.singatt_39, row.singatt_40, row.singatt_47, row.singatt_48, row.singatt_52, row.singatt_58, row.singatt_59]




            for j in backlist:
                backwards_score(j) #call my above-defined function
                negativelist = negativelist + [backscore]




        #Function stuff here



            newdf['enviro_school'][index] = (row.singatt_1 + row.singatt_2 + row.singatt_3 + row.singatt_5 + row.singatt_6 + row.singatt_7 + row.singatt_8 + row.singatt_9 + row.singatt_11 + row.singatt_12 + negativelist[0])/11


            newdf['enviro_home'][index] = (row.singatt_19 + row.singatt_22 + row.singatt_23 + row.singatt_24 + row.singatt_25 + row.singatt_27 + row.singatt_28)/7


            newdf['enviro_informal'][index] =(row.singatt_29 + row.singatt_30 + row.singatt_32 + row.singatt_33 + row.singatt_34)/5


            newdf['identity_self'][index] = (row.singatt_35 + row.singatt_37 + row.singatt_38 + negativelist[4] + negativelist[5] + row.singatt_43 + row.singatt_44 + row.singatt_45 + row.singatt_46 + negativelist[7] + row.singatt_49)/11


            newdf['identity_emotion'][index] =(row.singatt_13 + row.singatt_14 + row.singatt_16 + row.singatt_17+ row.singatt_50 + row.singatt_51+ row.singatt_53 + row.singatt_54 + row.singatt_55 + row.singatt_56 + negativelist[9])/11


            newdf['self_social'][index] = (row.singatt_4 + row.singatt_10 + row.singatt_15 + row.singatt_20 + row.singatt_21 + negativelist[1] + negativelist[2] + negativelist[3] +  row.singatt_41+ row.singatt_42 + negativelist[6] + negativelist[8] + row.singatt_57 + negativelist[10] + row.singatt_60)/15


        else:

             newdf['enviro_school'][index] = ''
             newdf['enviro_home'][index] = ''
             newdf['enviro_informal'][index] =''
             newdf['identity_self'][index] =''
             newdf['identity_emotion'][index]=''
             newdf['self_social'][index] =''





    newdf.to_csv(outfilename,index =False)
    print('congrats! you are now done with SINGING ATTITUDES scoring.')




if __name__ == '__main__': #do not change any part of this if statement (or below!!)

    # Map command line arguments to function arguments.
    try:
        score(*sys.argv[1:])
    except:
        print("you have run this incorrectly!To run, type:\n \
        'python3.7 [name of script].py [full path of RAW DATA] [full path of output folder]'")
