from machine import I2C
import struct, utime
import sys
from lib.lidar import LIDAR





i2c_0 = I2C(0, mode=I2C.MASTER, baudrate=400000, pins=('P7', 'P8'))
utime.sleep_ms(50)


slaves = i2c_0.scan()
if len(slaves) == 0:
    print('Err in bus 0, please check wiring')
    sys.exit()


freq = 0x64 # 0x64 100Hz, 0xFA 250Hz
lidar_0 = LIDAR(freq, i2c_0, slaves[0], 'Sens_0')


while(True):
    s0 = lidar_0.get_distance()
    t0 = lidar_0.get_temp()
    a0 = lidar_0.get_signal_amp()
    print(s0, t0, a0)
    utime.sleep_ms(50)
