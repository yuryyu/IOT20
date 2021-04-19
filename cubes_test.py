import paho.mqtt.client as mqtt
import time
import random
from mqtt_init import *


# broker IP adress:
broker=broker_ip
running_time = 30 # in sec
port=broker_port # for using web sockets
global ON
ON=False
TRH = 22.4

def on_log(client, userdata, level, buf):
        print("log: "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
def on_message(client,userdata,msg):
        global ON
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message received",m_decode)
        #if 'HUMIDITY' not in m_decode:
        ON=msg_parse(m_decode)
        send_msg(client)

def msg_parse(m_decode):
        print(m_decode)        
        rez=float(m_decode.split('Temperature: ')[1].split(' Humidity:')[0])
        #{"addr":0, "cname":"LDR", "value":1017}
        #{"addr":0, "cname":"TEMPERATURE", "value":32.00}
        # Temperature: 22.1 Humidity: 76.2
        if rez>TRH:
                return True
        return False

def send_msg(client):
        global ON
        # Following is an example for code turning a Relay device 'On':
        device_ID = "3PI_22559442/sts"
        # client.publish("matzi/0/3PI_22559442/sts", ' {"type":"set_state", "action":"set_value", "addr":0, "cname":"ONOFF", "value":1}') 
        if ON:
                client.publish("matzi/0/"+device_ID, ' {"type":"set_state", "action":"set_value", "addr":0, "cname":"ONOFF", "value":1}')                
        else:
                # and consequently 'OFF':
                client.publish("matzi/0/"+device_ID, ' {"type":"set_state", "action":"set_value", "addr":0, "cname":"ONOFF", "value":0}')
               

r=random.randrange(1,10000) # for creating unique client ID
clientname="IOT_test-"+str(r)
client = mqtt.Client(clientname, clean_session=True) # create new client instance

client.on_connect=on_connect  #bind call back function
client.on_disconnect=on_disconnect
#client.on_log=on_log
client.on_message=on_message
client.username_pw_set(username=username,password=password)


print("Connecting to broker ",broker)
client.connect(broker,int(port))     #connect to broker


# Next loop will publishing all messages during running time
client.loop_start()
client.publish('testtopic/778',"test1")
#client.subscribe("matzi/0/3PI_16145805/sts") # button ID
#client.subscribe("matzi/0/3PI_11310380/sts") # REED ID
#client.subscribe("matzi/0/3PI_3380731/sts") # Light ID
client.subscribe('testtopic/778') # DTH ID

#client.subscribe("matzi/#")
time.sleep(running_time)
client.loop_stop()
client.disconnect() # disconnect
print("End of script run")

