import os
import sys
import requests
import re
import RPi.GPIO as GPIO
from time import sleep

def get_website(website_url):
	er = 0
	headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; PIWEBMON)',
        'Cache-Control': 'no-cache' }
	try: response = requests.get(website_url, headers=headers, timeout = 10)
	except Exception as e: 
		er = 1

	if (response.status_code < 200 or response.status_code > 299 or er > 0):
		return -1, "Error"

	return 1, response.text

def main(i):
    website_status, html = get_website("http://192.168.1.47")

    if website_status == -1:
        print("Non 2XX response while fetching")
    t = float((re.findall(':.*:|$', html)[0]).strip(":"))
    print (i, t)


GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT) 

GPIO.output(8, True) 
sleep(5)
GPIO.output(8, False) 

i = 0
while True: 
	main(i)
	i += 1
	sleep(1)
