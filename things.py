from math import ceil
from crc import *
from my_serial import *
import time


class Relay:
    def __init__(self, id):
        self.id = id
        self.relay_ON = [0, 6, 0, 0, 0, 255, 0, 0]
        self.relay_OFF = [0, 6, 0, 0, 0, 0, 0, 0]
        self.relay_ON[0] = self.relay_OFF[0] = id
        add_crc16_modbus(self.relay_ON)
        add_crc16_modbus(self.relay_OFF)

    def data_format(self):
        print("Data for relay {} on is: {}".format(self.id, self.relay_ON))
        print("Data for relay {} off is: {}".format(self.id, self.relay_OFF))

    def turnRelayOn(self, ser):
        ser.write(self.relay_ON)
        print("On: {}".format(self.relay_ON))
        return serial_read_data(ser)

    def turnRelayOff(self, ser):
        ser.write(self.relay_OFF)
        print("Off: {}".format(self.relay_OFF))
        return serial_read_data(ser)


class MixerRelay(Relay):
    flow = 5  # 5 ml/s
    def __init__(self, id, fertilizer):
        self.fertilizer = fertilizer
        self.timer = ceil(self.fertilizer / self.flow)
        super().__init__(id)

    def turnRelayOn(self, ser):
        if self.timer > 0:
            super().turnRelayOn(ser)
        return
    
    def turnRelayOff(self, ser):
        if self.timer > 0:
            super().turnRelayOff(ser)
        return


class AreaRelay(Relay):
    def __init__(self, areaSelector):
        super().__init__(areaSelector + 3)  #id = area + 3 (ex: area 1 have id 4)


class PumpRelay(Relay):
    def __init__(self, id):
        super().__init__(id)


class Sensor:
    def __init__(self, id):
        self.id = id
        self.soil_temp = [0, 3, 0, 6, 0, 1, 0, 0]
        self.soil_humid = [0, 3, 0, 7, 0, 1, 0, 0]
        self.soil_temp[0] = self.soil_humid[0] = id
        add_crc16_modbus(self.soil_temp)
        add_crc16_modbus(self.soil_humid)

    def data_format(self):
        print("Data for temp senor {} is: {}".format(self.id, self.soil_temp))
        print("Data for humid sensor {} is: {}".format(self.id, self.soil_humid))

    def getTemp(self, ser):
        serial_read_data(ser)
        ser.write(self.soil_temp)
        print(self.soil_temp)
        time.sleep(1)
        return serial_read_data(ser)

    def getHumid(self, ser):
        serial_read_data(ser)
        ser.write(self.soil_humid)
        print(self.soil_humid)
        time.sleep(1)
        return serial_read_data(ser)

# try:
#     ser = serial.Serial(port=getPort(), baudrate=9600)
#     print(ser)
#     print("Open successfully")
# except:
#     print("Can not open the port")


# def main(args=None):
#     mixerRelay1 = MixerRelay(1, 20)
#     mixerRelay2 = MixerRelay(2, 10)
#     mixerRelay3 = MixerRelay(3, 20)

#     print("Timer for mixer {} is {}".format(mixerRelay1.id, mixerRelay1.timer))
#     print("Timer for mixer {} is {}".format(mixerRelay2.id, mixerRelay2.timer))
#     print("Timer for mixer {} is {}".format(mixerRelay3.id, mixerRelay3.timer))

#     mixerRelay1.data_format()
#     mixerRelay2.data_format()
#     mixerRelay3.data_format()

#     sensor = Sensor(10)
#     sensor.data_format()

#     sensor.getTemp(ser)


# if __name__ == '__main__':
#     main()