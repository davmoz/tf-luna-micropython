import struct, utime
import constants as const

class LIDAR:
    '''docstring for LIDAR.'''

    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr

    def addr(self):
        return self.addr,

    def save(self):
        self.i2c.writeto_mem(self.addr, const.SAVE, 0x01)
        utime.sleep_ms(100)

    def reboot(self):
        self.i2c.writeto_mem(self.addr, const.SHUTDOWN_REBOOT, 0x02)

    def _save_reboot(self):
        utime.sleep_ms(50)
        self.save()
        self.reboot()
        utime.sleep_ms(500)

    def distance(self):
        dist = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        return struct.unpack('<H', dist)[0]

    def temp(self):
        temp = self.i2c.readfrom_mem(self.addr, 0x04, 2)
        return int(struct.unpack('<H', temp)[0]) * 0.01

    def signal_amp(self):
        amp = self.i2c.readfrom_mem(self.addr, 0x02, 2)
        return int(struct.unpack('<H', amp)[0])

    def version_rev(self):
        v = self.i2c.readfrom_mem(self.addr, const.VERSION_REVISION, 3)
        return 'LiDAR Version {}.{}.{}'.format(v[2], v[1], v[0])

    def set_frequency(self, freq=0x64):
        self.i2c.writeto_mem(self.addr, const.FPS_LOW, freq)
        self._save_reboot()

    def power_saving_mode(self, power_saving_mode=True):
        val = 0x01 if power_saving_mode else 0x00
        self.i2c.writeto_mem(self.addr, const.LOW_POWER, val)

    def on_off(self, on=True):
        val = 0x00 if on else 0x01
        self.i2c.writeto_mem(self.addr, const.ENABLE, val)

    def reset(self):
        self.i2c.writeto_mem(self.addr, const.RESTORE_FACTORY_DEFAULTS, 0x01)
        self._save_reboot()

    def set_min_max(self, min, max):
        min *= 10
        max *= 10

        high, low  = min >> 8, min & 0XFF
        self.i2c.writeto_mem(self.addr, const.MIN_DIST_HIGH, high)
        self.i2c.writeto_mem(self.addr, const.MIN_DIST_LOW, low)

        high, low  = max >> 8, max & 0XFF
        self.i2c.writeto_mem(self.addr, const.MAX_DIST_HIGH, high)
        self.i2c.writeto_mem(self.addr, const.MAX_DIST_LOW, low)
        self._save_reboot()

    def read_all(self):
        return 'Distance {}, ChipTemp {}, SignalAmp {}'.format(
        self.distance(),
        self.temp(),
        self.signal_amp())
