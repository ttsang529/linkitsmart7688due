import time
import sys
import json
import paho.mqtt.client as mqtt
import os
mqtt_server_dns="172.16.2.143"


f = os.popen('ifconfig  apcli0| grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
local_ip=f.read().strip()

#get arduino data
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

#build up mqtt
mqttc=mqtt.Client()
mqttc.connect(mqtt_server_dns,8883,60)
#mqtt set username password
mqttc.username_pw_set("IOTDevice", "ubiqconndevicelogin")
#mqtt set crt
mqttc.tls_set('/root/ca.crt')
payload='{"mqtt":"Offline","device":"Linklt Smart 7688 Duo"}'
mqttc.will_set('IOT/Client',payload,qos=2, retain=False)
mqttc.loop_start()
def reading():
    h0 = value.get("h")
    t0 = value.get("t")
    t1 = value.get("touch")
    l0 = value.get("l")
    a =json.dumps({"Device":"Linklt Smart 7688 Duo","source":local_ip,"hum":h0,"temp":t0,"touch":t1,"light":l0})
    #print(a)
    return a
#mqtt begin send IOT/Client Connect
mqttc.publish("IOT/Client",'{"mqtt":"Online","device":"Linklt Smart 7688 Duo","source":"'+local_ip+'"}',2)
while 1:
   info=reading()
   (result,mid)=mqttc.publish("IOT/Data",info,2)
   time.sleep(1)
mqttc.loop_stop()
mqttc.disconnect()
