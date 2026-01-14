# tf-luna
A simple micropython i2c library for TF-Luna LiDAR Module.

**Repo-status**: See [Implemented functions](#implemented-functions)

## Important Note
This library requires **MicroPython** firmware to be installed on your microcontroller. If you get `ImportError: no module named 'machine'`, you need to install MicroPython firmware first. See [Getting Started](#getting-started) below.

## Getting started

### 1. Install MicroPython Firmware
Before using this library, make sure your board has MicroPython installed:
- **Raspberry Pi Pico / XIAO RP2040**: Download from [micropython.org/download/rp2-pico](https://micropython.org/download/rp2-pico/)
- **ESP32**: Download from [micropython.org/download/esp32](https://micropython.org/download/esp32/)
- **Other boards**: Check [micropython.org/download](https://micropython.org/download/)

### 2. Hardware Setup
To enable i2c mode on TF-Luna, connect **pin 5 to GND**. See [Datasheet](https://www.robotshop.com/media/files/content/b/ben/pdf/tf-luna-8m-lidar-distance-sensor-instructions-manual.pdf)

| Pin & Function        | Description        |
| --------------------- | ------------------ |
| 1 VCC                 | Vin (5V)           |     
| 2 RXD/SDA             | Receiving/Data     |
| 3 TXD/SCL             | Transmitting/Clock |     
| 4 GND                 | GND                |     
| 5 Configuration Input | Ground: I2C mode <br />/3.3V: Serial port <br />Communications mode |     
| 6 Multiplexing output | Default: on/off mode output<br />I2C mode: Data availability<br />signal on but not switching value mode     |

### 3. Upload Library Files
Copy the `lib` folder to your MicroPython board.

### 4. Choose the Right Example
Different MicroPython boards use different I2C initialization:

#### For XIAO RP2040 / Raspberry Pi Pico:
Use `example_rp2040.py`
```python
from machine import I2C, Pin
import time
from lib.lidar import LIDAR

# XIAO RP2040: Use GPIO0 (D4) and GPIO1 (D5)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lidar = LIDAR(i2c, 0x10)
```

#### For ESP32:
Use `example_esp32.py`
```python
from machine import I2C, Pin
import time
from lib.lidar import LIDAR

# ESP32: Default pins are GPIO22 (SCL) and GPIO21 (SDA)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lidar = LIDAR(i2c, 0x10)
```

#### For Pycom Boards (WiPy, LoPy, etc.):
Use `example_pycom.py`
```python
from machine import I2C
import utime
from lib.lidar import LIDAR

# Pycom boards use named pins
i2c = I2C(0, mode=I2C.MASTER, baudrate=400000, pins=('P7', 'P8'))
lidar = LIDAR(i2c, 0x10)
```

### 5. Wiring Examples

#### XIAO RP2040:
- TF-Luna VCC → 5V
- TF-Luna GND → GND
- TF-Luna RXD/SDA → D4 (GPIO0)
- TF-Luna TXD/SCL → D5 (GPIO1)
- TF-Luna Pin 5 → GND (enables I2C mode)

#### ESP32:
- TF-Luna VCC → 5V
- TF-Luna GND → GND
- TF-Luna RXD/SDA → GPIO21
- TF-Luna TXD/SCL → GPIO22
- TF-Luna Pin 5 → GND (enables I2C mode)

## Troubleshooting

### ImportError: no module named 'machine'
This means you don't have MicroPython installed. You need to:
1. Download the correct MicroPython firmware for your board
2. Flash it to your board using the appropriate tool
3. Reconnect and try again

### Bus error: Please check LIDAR wiring
If you see this error, check:
1. Pin 5 on TF-Luna is connected to GND (enables I2C mode)
2. SDA and SCL are connected to the correct pins for your board
3. VCC is connected to 5V and GND to GND
4. The I2C address is correct (default: 0x10)

### Device not found when scanning I2C
Run this code to scan for I2C devices:
```python
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(YOUR_SCL_PIN), sda=Pin(YOUR_SDA_PIN), freq=400000)
devices = i2c.scan()
print([hex(addr) for addr in devices])
```     


## Implemented functions
* Distance
* Chip temperature
* Signal Amplitude
* Set Min/Max range
* Reboot
* Reset to factory defaults
* Change sampling rate / freq

## To-Do
* Trigger mode
* Change slave address
* Tick
* Error
* UART
