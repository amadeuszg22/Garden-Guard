import machine
from machine import Pin
import time
import urequests as requests
import ujson
import esp
import dht

stime = (60000000 * 30)
def volt():
	p15 = machine.Pin(15, machine.Pin.OUT)
	p15.on()
	time.sleep(1)
	p15.off()
	
def mosure():
	id = "mo"
	p14 = Pin(14, Pin.OUT)
	p14.on()
	adc = machine.ADC(0)
	am = adc.read()
	mp = ((am / 1023.00) * 100)
	print("The ground moisure is:", mp, "%")
	feed(mp,id)
	p14.off()

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
		url ="https://io.adafruit.com/api/v2/Ama_g/feeds/mint-moisture/data.json"
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

while True:
	time.sleep(15)
	if machine.reset_cause() == machine.DEEPSLEEP_RESET:
		print('woke from a deep sleep')
	else:
		print('power on or hard reset')
	outtemp()
	outhum()
	volt()
	#mosure()
	#print("going sleep for:", stime)
	time.sleep(60)
	#esp.deepsleep(stime)

	