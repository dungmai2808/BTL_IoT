from things import *
import time


class Relay_Task:
    def __init__(self, fertilizer1, fertilizer2, fertilizer3, areaSelector, cycle, startTime):
        self.mixer1 = MixerRelay(1, fertilizer1)
        self.mixer2 = MixerRelay(2, fertilizer2)
        self.mixer3 = MixerRelay(3, fertilizer3)
        self.area = AreaRelay(areaSelector)
        self.pumpIn = PumpRelay(7)
        self.pumpOut = PumpRelay(8)
        self.cycle = cycle
        self.startTime = startTime
        self.state = 0
        self.isRelayActive = True

    def Relay_Execute(self, ser, timer, relay):
        if timer == 0:
            return
        time_slot = 5
        
        # if data has error, resend after 1s. After 5 times, notice error to user
        while time_slot > 0:
            relay.turnRelayOn(ser)
            if relay.return_data == 255:
                break
            time.sleep(1)
            time_slot = time_slot - 1
        if time_slot == 0:
            self.isRelayActive = False
            print("Maybe relay {} is not turn on, Please check....".format(relay.id))

        time.sleep(timer)

        time_slot = 5
        # if data has error, resend after 1s. After 5 times, notice error to user
        while time_slot > 0:
            relay.turnRelayOff(ser)
            if relay.return_data == 0:
                break
            time.sleep(1)
            time_slot = time_slot - 1
        if time_slot == 0:
            self.isRelayActive = False
            print("Maybe relay {} is not turn off, Please check....".format(relay.id))

        self.isRelayActive = True #delete when execute

    def Task_Execute(self, ser):
        self.isRelayActive = True
        self.state = 1
        while self.state != 0:
            if self.state == 1:
                self.Relay_Execute(ser, self.mixer1.timer, self.mixer1)
                if self.isRelayActive == False:
                    self.state = 0
                    return self.isRelayActive
                self.state = 2
            elif self.state == 2:
                self.Relay_Execute(ser, self.mixer2.timer, self.mixer2)
                if self.isRelayActive == False:
                    self.state = 0
                    return self.isRelayActive
                self.state = 3
            elif self.state == 3:
                self.Relay_Execute(ser, self.mixer3.timer, self.mixer3)
                if self.isRelayActive == False:
                    self.state = 0
                    return self.isRelayActive
                self.state = 4
            elif self.state == 4:
                self.Relay_Execute(ser, 5, self.pumpIn)
                if self.isRelayActive == False:
                    self.state = 0
                    return self.isRelayActive
                self.state = 5
            elif self.state == 5:
                self.Relay_Execute(ser, 5, self.area)
                if self.isRelayActive == False:
                    self.state = 0
                    return self.isRelayActive
                self.state = 6
            elif self.state == 6:
                self.Relay_Execute(ser, 5, self.pumpOut)
                if self.isRelayActive == False:
                    self.state = 0
                    return self.isRelayActive
                self.state = 0
                return self.isRelayActive
            else:
                self.state = 0
                return self.isRelayActive
            

class Sensor_Task:
    def __init__(self):
        self.sensor = Sensor(10)
        self.isSensorActive = True

    def Sensor_Execute(self, ser, type):
        if(type == "temp"):
            time_slot = 5
            # if data has error, resend after 1s. After 5 times, notice error to user
            while time_slot > 0:
                data = self.sensor.getTemp(ser) / 100
                print("Temp is", data)
                if data >= 0 and data <= 100:
                    return data
                time.sleep(1)
                time_slot = time_slot - 1
            if time_slot == 0:
                self.isSensorActive = False
                print("Maybe sensor {} is not working, Please check....".format(self.sensor.id))
                return 0
            
        elif(type == "humid"):
            time_slot = 5
            # if data has error, resend after 1s. After 5 times, notice error to user
            while time_slot > 0:
                data = self.sensor.getHumid(ser) / 100
                print("Humid is", data)
                if data >= 0 and data <= 100:
                    return data
                time.sleep(1)
                time_slot = time_slot - 1
            if time_slot == 0:
                self.isSensorActive = False
                print("Maybe sensor {} is not working, Please check....".format(self.sensor.id))
                return 0
               
        else:
            return 0

    def Task_Execute(self, ser):
        self.isSensorActive = True
        temp = 0
        counter = 10
        while counter > 0 and self.isSensorActive:
            temp = temp + self.Sensor_Execute(ser, "temp")
            counter = counter - 1
            time.sleep(1)
        if self.isSensorActive == False:
            return self.isSensorActive
        print("Temperature is:", temp/10)

        humid = 0
        counter = 10
        while counter > 0 and self.isSensorActive:
            humid = humid + self.Sensor_Execute(ser, "humid")
            counter = counter - 1
            time.sleep(1)
        if self.isSensorActive == False:
            return self.isSensorActive
        print("Humidity is:", humid/10)
        return self.isSensorActive


# isRelayActive = True

# try:
#     ser = serial.Serial(port=getPort(), baudrate=9600)
#     print(ser)
#     print("Open successfully")
# except:
#     print("Can not open the port")
# task1 = Task(20, 10, 20, 1, 1, 0)
# isRelayActive = task1.Task_Execute(ser)