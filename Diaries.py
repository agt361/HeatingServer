WDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

from config import *
import config as cf
from datetime import date, datetime, timedelta
import os
import shutil
#import plotly.express as px
import pandas as pd
import csv
from time import sleep
from tabulate import tabulate
from threading import Thread
import sys
import subprocess


def ClrScrn():
    os.system('clear')
#    print(BOLD)
        
def GetNewTemporary():
    while True:
        ClrScrn()
        print("New Temporary Entry\n")
        print("Enter start date and time\n")
        year = GetNumber(True,'Enter year: ', 2022, 2122)
        month = GetNumber(True,'Enter month: ',1,12)
        day = GetNumber(True,'Enter day: ',1,31)
        hours = GetNumber(True,'Enter hour: ',00,23)
        minutes = GetNumber(True,'Enter minutes: ',00,59)
        try:
            d = datetime(year, month, day, hours, minutes)
        except:
            print("\nNot a date - wait!")
            sleep(5)
            continue
        if d < BasicDate(datetime.now()):
            print("\nMust be a future date - wait!")
            sleep(5)
            continue
        break
    print(d)
    sd = d.strftime("%Y-%m-%d %H:%M")
    ClrScrn()
    print(sd)
    print("\n")
    txt = MyInput("Enter event name: ", 50)
    ClrScrn()
    print(sd, '\n',txt)
    print("\n")
    dh = GetNumber(True,'Enter duration hours: ',0,9)
    dm = GetNumber(True,'Enter duration minutes: ',0,59)
    d = datetime(2000, 1, 1, dh, dm)
    sdd = d.strftime("%H:%M")
    return [sd, txt,sdd]

def PutInNewTemporaryEntry(FileName):
    df = pd.read_csv(FileName)
    gnt = GetNewTemporary()
    df.loc[-1] = gnt

    df.sort_values(by=['DateTime'], inplace=True)
    SaveFile(df,FileName)

def DoTemporaryEntries(Name):
    while (True):
        ClrScrn()
        print("Temporary Diary for ",Name,"\n" ,sep ='')
        FileName = "Temporary.csv"
        df = GetFile(FileName)
        indx = df[pd.to_datetime(df['DateTime']) < BasicDate(datetime.now())].index
        df.drop(indx , inplace=True)
        it = iter((1,2,3,4,5,6,7,8,9,10,11,12,13,14))
        print(tabulate(df, showindex=it, headers=df.columns))
        print("\n")
        y= GetNumber(True,'Enter 1 (new entry), 2 (delete entry) or 0 (leave): ', 0, 2)
        if (y == 1):
            PutInNewTemporaryEntry(FileName)
        if (y == 2):
            print('\nEnter number of row to delete or \n')
            z = GetNumber(True,'0 to abort: ', 0,len(df)) 
            if z > 0:
                df.drop(z-1,axis=0,inplace=True)
                SaveFile(df,FileName)
        if (y == 0):
           return

def GetNewPermanent():
    ClrScrn()
    print("New Permanent Entry\n")
    print("Enter start time\n")
    hours = GetNumber(True,'Enter hour: ',00,23)
    minutes = GetNumber(True,'Enter minutes: ',00,59)
    d = datetime(2000,1,1,hours, minutes)
    sd = d.strftime("%H:%M")

    ClrScrn()
    print(sd,'\n',sep='')
    DoW = GetNumber(True,"Enter day of week (1 = Mon to 7 = Sun): ", 1, 7)
    DoWeek = WDays[DoW-1]
 
    ClrScrn()
    print(sd, "\n", DoWeek,"\n",sep='')
    txt = MyInput("Enter event name: ", 50)
 
    ClrScrn()
    print(sd,'\n',DoWeek,'\n',txt,'\n',sep='')
    dh = GetNumber(True,'Enter duration hours: ',0,9)
    dm = GetNumber(True,'Enter duration minutes: ',0,59)
    d = datetime(2000, 1, 1, dh, dm)
    sdd = d.strftime("%H:%M")

    pattern = "xxxxx"
    while (pattern.count('n')+pattern.count('Y') != 5):
        ClrScrn()
        print(sd, '\n',DoWeek,'\n',txt,'\n\b',sdd,'\n',sep='')
        pattern = MyInput("Enter weeks of month (eg 'YnYnY') :xxxxx:\b\b\b\b\b\b", 5)
        pattern = pattern.replace('y','Y')
        pattern = pattern.replace('N','n')
    return [txt,DoWeek,sd,sdd,pattern,DoW," "]

def PutInNewPermanentEntry(FileName,Name):
    df = pd.read_csv(FileName)
    BlankOldIgnores(df)
    gnt = GetNewPermanent()
    df.loc[-1] = gnt
    df.sort_values(by=['DoW','Time'], inplace=True)
    SaveFile(df,FileName)

def BlankOldIgnores(df):
    for i in range(len(df)):
        try:
            ignoredate = BasicDate(pd.to_datetime(df.loc[i,'Ignore']))
        except:
            ignoredate = BasicDate(datetime(2000,1,1,1,1))
        if ignoredate < BasicDate(datetime.now()):
            df.loc[i,'Ignore'] = ' '

def BasicDate(x):
	return datetime.combine(x, datetime.min.time())
    
def DoPermanentEntries(Name):
    while (True):
        ClrScrn()
        print("Permanent Diary for ",Name,"\n" ,sep ='')
        FileName = "Permanent.csv"
        df = GetFile(FileName)
        BlankOldIgnores(df)
        df1 = df.drop('DoW', axis = 1)

        it = iter((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
        print(tabulate(df1, showindex=it, headers=df1.columns))
#        print(tabulate(df1, showindex=True, headers=df1.columns))
        print("\n")
        y= GetNumber(True,'Enter 1 (new entry), 2 (delete entry), 3 (ignore) or 0 (leave): ', 0, 3)
        if (y == 1):
            PutInNewPermanentEntry(FileName,Name)
        if (y == 2):
            print('\nEnter number of row to delete or \n')
            z = GetNumber(True,'0 to abort: ', 0,len(df)) 
            if z > 0:
                df.drop(z-1,axis=0,inplace=True)
                SaveFile(df,FileName)
        if (y == 3):
            print("\nEnter number of row for 'ignore' status change or\n")
            z = GetNumber(True,'0 to abort: ', 0,len(df))
            if z > 0:
                thisignore = df.loc[z-1,'Ignore']
                if thisignore == ' ':
                    print("Enter date to be ignored\n")
                    year = GetNumber(True,'Enter year: ', 2022, 2122)
                    month = GetNumber(True,'Enter month: ',1,12)
                    day = GetNumber(True,'Enter day: ',1,31)
                    try:
                        d = datetime(year, month, day, 0, 0)
                    except:
                        print("\nNot a date - wait!")
                        sleep(5)
                        continue
                    if d < datetime.now():
                        print("\nMust be a future date - wait!")
                        sleep(5)
                        continue
                    dow = d.weekday()
                    if dow + 1 != df.loc[z-1,'DoW']:
                        print("\nNot a "+df.loc[z-1,'Day of Week']+" - wait!")
                        sleep(5)
                        continue
                    sd = d.strftime("%Y-%m-%d")
                else:
                    sd = ' '
                df.loc[z-1,'Ignore'] = sd
                SaveFile(df,FileName)
        if (y == 0):
           return
            
def DoDiaries(Name):
    ClrScrn()
    while (True):
        ClrScrn()
        print("Heating Control Diaries for ",Name,"\n\n" ,sep ='')
        y = GetNumber(True,'Enter 1 (Permanent Diary), 2 (Temporary Diary) or 0 (Leave): ', 0,2)
        if y == 1:
            thread = Thread(target=DoPermanentEntries(Name))
            thread.start()
            # wait for the thread to finish
            thread.join()
        if y == 2:
            thread = Thread(target=DoTemporaryEntries(Name))
            thread.start()
            # wait for the thread to finish
            thread.join()
        if y == 0:
            return
