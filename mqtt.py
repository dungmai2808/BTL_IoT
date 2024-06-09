import sys
from Adafruit_IO import MQTTClient
import time
import json
from data import *

AIO_FEED_ID = ["scheduler", "deletesch", "broken", "sensor"]
AIO_USERNAME = "Vy2003"
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    global isRelayActive, isSensorActive

    print("Nhan du lieu: " + payload)
    if feed_id == "scheduler": #add scheduler
        temp_data = json.loads(payload)
        nodeSch = RNodeScheduler(temp_data)
        waitingList.add(nodeSch)
        waitingList.print_list()
    if feed_id == "deletesch": #delete scheduler
        waitingList.delete(payload)
        waitingList.print_list()
    if feed_id == "broken":
        if payload != "0":
            isRelayActive = False
        else:
            isRelayActive = True
    if feed_id == "sensor":
        if payload != "0":
            isSensorActive = False
        else:
            isSensorActive = True

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

client.publish("broken", 0)  #hư thì gửi khác 0
client.publish("sensor", 0)  #hư thì gửi 1


try:
    ser = serial.Serial(port=getPort(), baudrate=9600)
    print(ser)
    print("Open successfully")
except:
    print("Can not open the port")

isRelayActive = True
isSensorActive = True
waitingList = LinkedList()
sensorNode = SNodeScheduler("Scheduler 0", datetime.now() + timedelta(seconds=10))
waitingList.add(sensorNode)
next_sensor_execute = datetime.now() + timedelta(seconds=5)

while True:
    if not isSensorActive and not isRelayActive:
        # if both sensor and relays have error, wait 1s before checking again
        time.sleep(1)

    elif isSensorActive and isRelayActive:
        if datetime.now() < waitingList.head.startTime:
            # if not up to now, wait 1s before checking again
            time.sleep(1)
        else:
            currentNode = waitingList.head
            if currentNode.type == "relay":
                isRelayActive = currentNode.task.Task_Execute(ser)
            elif currentNode.type == "sensor":
                isSensorActive = currentNode.task.Task_Execute(ser)

            if currentNode.type == "relay" and isRelayActive:
                print("{}: {} is done".format(datetime.now(), currentNode.name))
                currentNode.cycle = currentNode.cycle - 1
                # if relay task do all its cycle
                if currentNode.cycle <= 0:
                    currentNode.startTime = currentNode.task.startTime + timedelta(days=1)
                    currentNode.cycle = currentNode.task.cycle
                else:
                    currentNode.startTime = datetime.now()
                # if current node was not deleted, delete and add again
                if waitingList.isAvailable(currentNode.name):
                    waitingList.delete(currentNode.name)
                    currentNode.next = None
                    waitingList.add(currentNode)
            elif currentNode.type == "sensor" and isSensorActive:
                next_sensor_execute = currentNode.startTime = currentNode.startTime + timedelta(minutes=2)
                waitingList.delete(currentNode.name)
                currentNode.next = None
                waitingList.add(currentNode)
            waitingList.print_list()    

    elif isRelayActive:
        currentNode = waitingList.findFirst("relay")
        if datetime.now() < currentNode.startTime:
            time.sleep(1)
        else:
            isRelayActive = currentNode.task.Task_Execute(ser)
            if isRelayActive:
                print("{}: {} is done".format(datetime.now(), currentNode.name))
                currentNode.cycle = currentNode.cycle - 1
                # if relay task do all its cycle
                if currentNode.cycle <= 0:
                    currentNode.startTime = currentNode.task.startTime + timedelta(days=1)
                    currentNode.cycle = currentNode.task.cycle
                else:
                    currentNode.startTime = datetime.now()
                # if current node was not deleted, delete and add again
                if waitingList.isAvailable(currentNode.name):
                    waitingList.delete(currentNode.name)
                    waitingList.add(currentNode)  
                    currentNode.next = None
                    waitingList.print_list()

    else: # isSensorActive == True
        if datetime.now() < next_sensor_execute:
            time.sleep(1)
        else:
            currentNode = waitingList.findFirst("sensor")
            isSensorActive = currentNode.task.Task_Execute(ser)
            if isSensorActive:
                next_sensor_execute = currentNode.startTime = currentNode.startTime + timedelta(minutes=2)
                waitingList.delete(currentNode.name)
                currentNode.next = None
                waitingList.add(currentNode)
                waitingList.print_list()