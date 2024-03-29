WDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

from pytimedinput import timedInput
from datetime import datetime, timedelta
import os
import shutil
import pandas as pd
import csv
from time import sleep
from tabulate import tabulate
from threading import Thread
import sys
import subprocess
from config import *
#BaseTime = datetime(2000,1,1,1,1)


def GetNumberFloat(flag,text,mn,mx):
    y = -1
    while y > mx or y < mn:
        if flag:
            y = float(MyInput(text,6))
        else:
            y = float(input(text))
        if y > mx or y < mn:
            LineUpandClear(1)
    return y

def ClrScrn():
    os.system('clear')
    print(BOLD)
        
            
def SaveOverride(xs1,xs2):
    x = datetime.now()
    xslf = x.strftime("%Y%m%d%H%M%S")
    filenamel = '/home/pi/shared/OFlag.csv'
    filenamed = 'OFlag'+xslf+'.csv'
    with open(filenamel, 'w') as f:
        f.write(f"KeepOnTill,KeepOffTill\n" )
        f.write(f"{xs1},{xs2}\n" )
    shutil.copyfile(filenamel,filenamed)
    while True:
        CTF = "States.csv"
        df = pd.read_csv(CTF)
        conf = datetime.strptime(df.loc[0,'Confirmed'],'%Y/%m/%d %H:%M:%S')
        if conf > x: return
        sleep(1)
        print("Waiting for confirmation...")


def DoOverrides(Name):
    ClrScrn()
    while (True):
        ClrScrn()
        df = GetFile("States.csv")

        KOnT = datetime.strptime(df.loc[0,'KeepOnTill'],'%Y/%m/%d %H:%M:%S')
        KOffT = datetime.strptime(df.loc[0,'KeepOffTill'],'%Y/%m/%d %H:%M:%S')

        print("Heating overrides for ",Name,"\n" ,sep ='')
        if KOnT > datetime.now():
            print ("Heating overridden to ON until",KOnT,'\n')
            j = GetNumber(True,"Do you want to cancel this? 0 (No) 1 (Yes): ",0,1)
            if j < 1: return
            else: 
                x = datetime.now()
                xsl = x.strftime("%Y/%m/%d %H:%M:%S")
                SaveOverride(xsl,xsl)
        elif KOffT > datetime.now():
            print ("Heating overridden to OFF until",KOffT,'\n')
            j = GetNumber(True,"Do you want to cancel this? 0 (No) 1 (Yes): ",0,1)
            if j < 1: return
            else: 
                x = datetime.now()
                xsl = x.strftime("%Y/%m/%d %H:%M:%S")
                SaveOverride(xsl,xsl)
        else:
            print ("No heating overrides\n")
            j = GetNumber(True,"Do you want enter an override 0 (No) 1 (Yes): ",0,1)
            if j < 1: return
            else: 
                j = GetNumber(True,"1 (ON), 2 (OFF) or 0 (leave): ",0,2)
                if j == 0: return
                if j == 1:
                    hoursx = GetNumber(True,'Enter ON period hour: ',00,23)
                    minutesx = GetNumber(True,'Enter ON period minutes: ',00,59)
                    x = datetime.now() + timedelta(hours = hoursx, minutes = minutesx)
                    xsl1 = x.strftime("%Y/%m/%d %H:%M:%S")
                    x = datetime.now() 
                    xsl2 = x.strftime("%Y/%m/%d %H:%M:%S")
                    SaveOverride(xsl1,xsl2)
                if j == 2:
                    x = datetime.now() + timedelta(hours = 1, minutes = 0)
                    xsl2 = x.strftime("%Y/%m/%d %H:%M:%S")
                    x = datetime.now() 
                    xsl1 = x.strftime("%Y/%m/%d %H:%M:%S")
                    SaveOverride(xsl1,xsl2)

