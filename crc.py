def crc16_modbus(data):
    crc = 0xFFFF
    split_data = data[:-2]
    for pos in split_data:
        crc ^= pos
        for i in range(8):
            if (crc & 0x0001):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

 
def add_crc16_modbus(data):
    crc = crc16_modbus(data)
    data[-1] = crc >> 8
    data[-2] = crc % 256


def check_crc16_modbus(data):
    crc = crc16_modbus(data)
    return (crc == (data[-2] | data[-1] << 8))