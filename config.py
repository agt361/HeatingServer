import os
import shutil
import pandas as pd
import csv
from pytimedinput import timedInput
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NaveIP = os.getenv('NaveIP')
NavePicoIP = os.getenv('NavePicoIP')
NaveClientPicoIP = os.getenv('NaveClientPicoIP')
ChancelIP = os.getenv('ChancelIP')
ChancelPicoIP = os.getenv('ChancelPicoIP')
ChancelClientPicoIP = os.getenv('ChancelClientPicoIP')

Picourl = pd.Series( [NavePicoIP, NaveClientPicoIP, ChancelPicoIP, ChancelClientPicoIP], \
            index=['Nave', 'NaveClient', 'Chancel', 'ChancelClient'])

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
BOLD = '\033[1m'
GhostFile = "/home/pi/shared/Ghost.csv"

def SaveFile(df,FileName):
    with open(GhostFile, 'w') as csv_file:
        df.to_csv(path_or_buf=csv_file, index = False)
    shutil.copyfile(GhostFile,FileName)
#    x = datetime.now()
#    xsl = x.strftime("%y%m%d%H%M%S")
#    CTFR = 'Flag'+xsl
#    CTF = "/home/pi/shared/Flag"
#    shutil.copyfile(CTF,CTFR)

def GetFile(filename):
    return pd.read_csv(filename)

def my_int(text,mx):
    try: y = int(text)
    except: y = mx+1
    return(y)

def MyInput(text,ml):
    userText, timedOut = timedInput(text, timeout=120, maxLength = ml)
    if timedOut:
        sys.exit()
    return userText 
    
def LineUpandClear(i):
    for j in range(i):
        print(LINE_UP, BOLD, end=LINE_CLEAR)

def GetNumber(flag,text,mn,mx):
    y = -1
    while y > mx or y < mn:
        if flag:
            y = my_int(MyInput(text,6),mx)
        else:
            y = my_int(input(text),mx)
        if y > mx or y < mn:
            LineUpandClear(1)
    return y