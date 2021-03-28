import struct
import constants as const

class LIDAR:
    """docstring for LIDAR."""

    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = int("0x%X" % addr)

    def _save(self):
        self.i2c.writeto_mem(self.addr, const.SAVE, 0x01)

    def get_addr(self):
        return self.addr

    def get_distance(self):
        dist = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        return struct.unpack('<h', dist)[0]

    def get_temp(self):
        temp = self.i2c.readfrom_mem(self.addr, 0x04, 2)
        return int(struct.unpack('<h', temp)[0]) * 0.01

    def get_signal_amp(self):
        amp = self.i2c.readfrom_mem(self.addr, 0x02, 2)
        return int(struct.unpack('<h', amp)[0])

    def set_frequency(self, freq=0x64):
        self.i2c.writeto_mem(self.addr, 0x26, freq)

    def power_saving_mode(self, power_saving_mode=True):
        val = 0x01 if power_saving_mode else 0x00
        self.i2c.writeto_mem(self.addr, const.LOW_POWER, val)

    def reboot(self):
        self.i2c.writeto_mem(self.addr, const.SHUTDOWN_REBOOT, 0x02)

    def on_off(self, on=True):
        val = 0x00 if on else 0x01
        self.i2c.writeto_mem(self.addr, const.ENABLE, val)
