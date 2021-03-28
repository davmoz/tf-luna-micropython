from machine import I2C
import utime, struct

class LIDAR:
    """docstring for LIDAR."""

    def __init__(self, freq, i2c, slave_addr, name):
        self.i2c = i2c
        self.slave_addr = "0x%X" % slave_addr
        self.name = name
        self.i2c.writeto_mem(int(self.slave_addr), 0x26, freq)

    def get_addr(self):
        return self.slave_addr

    def get_name(self):
        return self.name

    def get_distance(self):
        dist = self.i2c.readfrom_mem(int(self.slave_addr), 0x00, 2)

        return struct.unpack('<h', dist)[0]

    def get_temp(self):
        temp = self.i2c.readfrom_mem(int(self.slave_addr), 0x04, 2)
        return int(struct.unpack('<h', temp)[0]) * 0.01 
    #
    def get_signal_amp(self):
        amp = self.i2c.readfrom_mem(int(self.slave_addr), 0x02, 2)
        return int(struct.unpack('<h', amp)[0])

    def sleep(self):
        pass
    def awake(self):
        pass
