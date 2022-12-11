from pytimedinput import timedInput
from datetime import date, datetime, timedelta
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
import config as cf

WDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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
        
            
def DoSystem(Name):
    ClrScrn()
    while (True):
        ClrScrn()
        print("Heating parameters for ",Name,"\n" ,sep ='')
        FileName = "System.csv"
        df = GetFile(FileName)
        print('Target temerature:', float(df.loc[0,'Target Temperature']),'\n')
        print('Background temerature:', float(df.loc[0,'Background Temperature']),'\n')
        print('Hysteresis (full cycle):', float(df.loc[0,'Hysteresis']),'\n')
        print('Thermal Lag:', float(df.loc[0,'Thermal Lag']),'\n')

        y = GetNumber(True,'Enter 1 (Target), 2 (Background) 3 (Hysteresis) 4 (Thermal Lag) 0 (Leave): ', 0,4)
        if y == 1:
            df.loc[0,'Target Temperature'] = GetNumberFloat(True,"\nEnter Target Temperature: ", 1, 30)
        if y == 2:
            df.loc[0,'Background Temperature'] = GetNumberFloat(True,"\nEnter Background Temperature: ", 1, 25)
        if y == 3:
            df.loc[0,'Hysteresis'] = GetNumberFloat(True,"\nEnter Hysteresis: ", 0.1, 2)
        if y == 4:
            df.loc[0,'Thermal Lag'] = GetNumberFloat(True,"\nEnter Thermal Lag: ", 0.1, 2)
        df.loc[0,'PicoIP'] = cf.Picourl[Name]
        df.loc[0,'PicoClientIP'] = cf.Picourl[Name+'Client']
        SaveFile(df,FileName)
        if y == 0:
            return
 
