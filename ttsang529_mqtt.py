from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
import json
import datetime

# Read in command-line parameters
#https://us-west-2.console.aws.amazon.com/iotv2/home?region=us-west-2#/thing/sensingData
host = "a2ezaog8yauwgu.iot.us-west-2.amazonaws.com"
rootCAPath = "/root/root-CA.crt"
certificatePath = "/root/sensingData.cert.pem"
privateKeyPath = "/root/sensingData.private.key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("publish")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()

sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

# Publish to the same topic in a loop forever
while True:
	humidity = value.get("h")
	temperature = value.get("t")
        touch = value.get("touch")
	light = value.get("l")
	print "Humi: " + humidity
        print "Temp: " + temperature
        print "touch: " + touch
        print "light: " + light
	t = time.time();
	date = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
	print "humidity: %d, temperature: %d touch: %d light: %d" % (float(humidity), float(temperature), float(touch) ,float(light))
	myAWSIoTMQTTClient.publish("sensingData/TemperatureHumidity/Room1", json.dumps({"time": date, "temperature": temperature, "humidity": humidity , "touch" : touch , "light":light,"location":"room1" }), 1)
	time.sleep(1)