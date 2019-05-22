import machine
from machine import Pin
import time
import urequests as requests
import ujson
import esp
import dht

class setup():
	stime = (60000000 * 30)
	p15 = machine.Pin(15, machine.Pin.OUT)
	p15.off()
	p14 = Pin(14, Pin.OUT)
	p14.off()

def volt():
	id ="volt"
	#setup.p15.on()
	time.sleep(2)
	volta = machine.ADC(0)
	volts = volta.read()
	v =  ((4.82 / 1023.00) * volts)
	print ("Battery voltage is:",volts,"V")
	feed(v,id)
	#setup.p15.off()
	
	
def mosure():
	id = "mo"
	setup.p15.on()
	setup.p14.on()
	adc = machine.ADC(0)
	am = adc.read()
	mp = ((am / 1023.00) * 100)
	print (am)
	print("The ground moisure is:", mp, "%")
	feed(mp,id)
	setup.p14.off()
	setup.p15.off()

def outtemp():
	id = "temp"
	d = dht.DHT22(machine.Pin(4))
	d.measure()
	print ("Out side temperature is: ", d.temperature(),"C")
	feed(d.temperature(),id)

def outhum():
	id = "hum"
	d = dht.DHT22(machine.Pin(4))
	d.measure()
	print ("Out side Humidity is: ", d.humidity(),"%")
	feed(d.humidity(),id)

def feed(value,mo):
	if mo == "mo":
		url ="https://io.adafruit.com/api/v2/Ama_g/feeds/star-moisture/data.json"
		headers = {'X-AIO-Key': '98d75633ba0440bebfe5840eedb09847','Content-Type': 'application/json'}
		data = '{"value": "'+str(value)+'"}'
		r = requests.post(url, data=data, headers=headers)
		results = r.json()
		print(results)
	if mo == "temp":
		url ="https://io.adafruit.com/api/v2/Ama_g/feeds/outtemp/data.json"
		headers = {'X-AIO-Key': '98d75633ba0440bebfe5840eedb09847','Content-Type': 'application/json'}
		data = '{"value": "'+str(value)+'"}'
		r = requests.post(url, data=data, headers=headers)
		results = r.json()
		print(results)
	if mo == "hum":
		url ="https://io.adafruit.com/api/v2/Ama_g/feeds/outhum/data.json"
		headers = {'X-AIO-Key': '98d75633ba0440bebfe5840eedb09847','Content-Type': 'application/json'}
		data = '{"value": "'+str(value)+'"}'
		r = requests.post(url, data=data, headers=headers)
		results = r.json()
		print(results)
	if mo == "volt":
		url ="https://io.adafruit.com/api/v2/Ama_g/feeds/voltage/data.json"
		headers = {'X-AIO-Key': '98d75633ba0440bebfe5840eedb09847','Content-Type': 'application/json'}
		data = '{"value": "'+str(value)+'"}'
		r = requests.post(url, data=data, headers=headers)
		results = r.json()
		print(results)

while True:
	setup()
	time.sleep(15)
	if machine.reset_cause() == machine.DEEPSLEEP_RESET:
		print('woke from a deep sleep')
	else:
		print('power on or hard reset')
	mosure()
	outtemp()
	outhum()
	volt()
	print("going sleep for:", setup.stime)
	time.sleep(30)
	esp.deepsleep(setup.stime)

	
