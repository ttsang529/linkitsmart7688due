import time
import sys
import json
import paho.mqtt.client as mqtt

#get arduino data
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

#build up mqtt
mqttc=mqtt.Client()
mqttc.connect("172.16.2.143",8883,60)
mqttc.loop_start()
def reading():
    h0 = value.get("h")
    t0 = value.get("t")
    t1 = value.get("touch")
    l0 = value.get("l")
    a =json.dumps({"hum":h0,"temp":t0,"touch":t1,"light":l0})
    print(a)
    return a
while 1:
   info=reading()
   (result,mid)=mqttc.publish("OTA/Broadcast",info,2)
   time.sleep(1)
mqttc.loop_stop()
mqttc.disconnect()
