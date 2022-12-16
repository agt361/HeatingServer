from Diaries import *
from Systems import *
from Overrides import *
from subprocess import Popen, PIPE
import pandas as pd
import time
import requests
import os
from config import *
import config as cf

def DoMenu(TName):
	os.chdir("/home/pi/shared/"+TName)
	while True:
		ClrScrn()
		print(TName," options\n")
		i = GetNumber(True,"1 (Diaries), 2 (Parameters), 3 (Override), 0 (Leave): ",0,3)
		if i == 1:
			DoDiaries(TName)
		if i == 2:
			DoSystem(TName)
		if i == 3:
			DoOverrides(TName)
		if i == 0:
			return

def ShowStatus(name):
#	CTFR = 'pi@'+TIP+':/home/pi/shared/CurrentTemperature.csv'
	CTF = "/home/pi/shared/"+name+"/CurrentTemperature.csv"
#	subprocess.run(['scp', CTFR, CTF],
#					stdout=subprocess.DEVNULL,
#					stderr=subprocess.DEVNULL)
	df = pd.read_csv(CTF)
	print(name.upper()+'\n')
	print(tabulate(df, showindex=False, headers=df.columns))
	print('\n')
#	navetemp = df.loc[0,'Temperature']
#	navedat =  df.loc[0,'DateTime']
#	if df.loc[0,'Heating On'] == True: naveho = 'Heating On'
#	else: naveho = 'Heating Off'
#	print(f'\nCurrent {name} Temperature is {navetemp} at {navedat}, {naveho}\n')
	
while True:
	os.chdir("/home/pi/shared")	
	ClrScrn()
	try:
		ShowStatus("Nave")
	except:
		pass
	try:
		ShowStatus("Chancel")
	except:
		pass
	i = GetNumber(True,"\n1 (Nave), 2 (Chancel), 3 (Refresh), 0 (Exit) ",0,3)
	if i == 1: DoMenu('Nave')
	if i == 2: DoMenu('Chancel')
	if i == 0: 
		exit(0)
