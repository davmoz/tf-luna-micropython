from machine import I2C
import struct, utime
import sys
from lib.lidar import LIDAR

LIDAR_ADDRESS = 0x10

i2c_0 = I2C(0, mode=I2C.MASTER, baudrate=400000, pins=('P7', 'P8'))
utime.sleep_ms(50)

slaves = i2c_0.scan()

# TF-Luna has the default slave_address 0x10
if LIDAR_ADDRESS not in slaves:
    print('Bus error: Please check LIDAR wiring')
    sys.exit()

lidar_0 = LIDAR(i2c_0, LIDAR_ADDRESS)

while(True):
    s0 = lidar_0.get_distance()
    t0 = lidar_0.get_temp()
    a0 = lidar_0.get_signal_amp()
    print(s0, t0, a0)
    utime.sleep_ms(20)
