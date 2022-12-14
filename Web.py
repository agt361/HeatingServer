import pandas as pd
from time import sleep
import os

os.chdir("/home/pi/shared/HeatingServer/")
while True:
	
	name = 'Chancel'

	OFile = name+".txt"

	CTF = "/home/pi/shared/"+name+"/CurrentTemperature.csv"
	df = pd.read_csv(CTF)

	with open(OFile, 'w') as f:
		f.write('\nSt Vigor '+name+' Heating\n')
		f.write(f"""
Date and Time: {df.loc[0,'DateTime']} 

Temperature:   {df.loc[0,'Temperature']} *C

Heating On:    {df.loc[0,'Heating On']} 

Rads ON:       {df.loc[0,'Rads On']}

Switch:        {df.loc[0,'Switch']}

Sensor:        {df.loc[0,'Sensor']}

Event:         {df.loc[0,'Event']}

""")

	sleep(120)
    

