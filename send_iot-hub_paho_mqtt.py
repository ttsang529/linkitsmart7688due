#!/usr/bin/python

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl

auth = {
  'username':"OTADevice",
  'password':"ubiqconndevicelogin"
}

tls = {
  'ca_certs':"/root/ca.crt",
  'tls_version':ssl.PROTOCOL_TLSv1
}

publish.single("OTA/Broadcast",
  payload="hello world",
  hostname="172.16.2.143",
  client_id="test",
  auth=auth,
  tls=tls,
  port=8883,
  protocol=mqtt.MQTTv311)
