"""
TF-Luna LiDAR Example - Generic MicroPython

This example demonstrates how to use the TF-Luna LiDAR sensor with MicroPython.
Different MicroPython boards have different I2C initialization syntax.

For board-specific examples, see:
- example_rp2040.py (for Raspberry Pi Pico, XIAO RP2040, etc.)
- example_esp32.py (for ESP32 boards)
- example_pycom.py (for Pycom boards like WiPy, LoPy, etc.)

IMPORTANT: Make sure you have MicroPython firmware installed on your board!
If you get "ImportError: no module named 'machine'", you may need to install
MicroPython firmware on your board first.
"""

from machine import I2C, Pin
import time
from lib.lidar import LIDAR

# TF-Luna has the default slave_address 0x10
LIDAR_ADDRESS = 0x10

# === CONFIGURE YOUR I2C PINS HERE ===
# Adjust these pin numbers for your specific board
# For RP2040 (Pico, XIAO RP2040): use Pin numbers like Pin(0), Pin(1)
# For ESP32: use Pin numbers like Pin(21), Pin(22)

SDA_PIN = 0  # Change to your SDA pin number
SCL_PIN = 1  # Change to your SCL pin number

# Initialize I2C
# Standard MicroPython I2C initialization (works on RP2040, ESP32, etc.)
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
time.sleep_ms(50)

# Scan for devices
slaves = i2c.scan()
print(f"I2C devices found: {[hex(addr) for addr in slaves]}")

if LIDAR_ADDRESS not in slaves:
    print('Bus error: Please check LIDAR wiring')
    print('Expected device address: 0x{:02x}'.format(LIDAR_ADDRESS))
    import sys
    sys.exit()

# Initialize LIDAR
lidar = LIDAR(i2c, LIDAR_ADDRESS)
print(lidar.version())

# Output limit when out of range
# Output only when between 20cm and 150cm (Up to 800cm)
lidar.set_min_max(20, 150)

lidar.set_frequency(250)

# Main loop - read distance continuously
while True:
    print(lidar.distance())
    time.sleep_ms(10)
