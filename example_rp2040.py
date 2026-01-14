"""
TF-Luna LiDAR Example for RP2040 Boards
Compatible with: Raspberry Pi Pico, XIAO RP2040, RP2040-based boards

Pin Configuration for XIAO RP2040:
- I2C0 SDA: GPIO 0 (D4)
- I2C0 SCL: GPIO 1 (D5)
- I2C1 SDA: GPIO 6 (D6)
- I2C1 SCL: GPIO 7 (D7)

Pin Configuration for Raspberry Pi Pico:
- I2C0 SDA: GPIO 0 or GPIO 4, 8, 12, 16, 20
- I2C0 SCL: GPIO 1 or GPIO 5, 9, 13, 17, 21
- I2C1 SDA: GPIO 2 or GPIO 6, 10, 14, 18, 26
- I2C1 SCL: GPIO 3 or GPIO 7, 11, 15, 19, 27

Wiring for TF-Luna:
1. VCC  -> 5V (or 3.3V depending on your board power supply)
2. RXD/SDA -> Connect to SDA pin
3. TXD/SCL -> Connect to SCL pin
4. GND  -> GND
5. Configuration Input -> GND (to enable I2C mode)
"""

from machine import I2C, Pin
import time
import sys
from lib.lidar import LIDAR

# TF-Luna has the default slave_address 0x10
LIDAR_ADDRESS = 0x10

# Configure I2C pins for XIAO RP2040
# Using I2C0 with GPIO0 (SDA) and GPIO1 (SCL)
SDA_PIN = 0  # D4 on XIAO RP2040
SCL_PIN = 1  # D5 on XIAO RP2040

# For Raspberry Pi Pico, you might use:
# SDA_PIN = 4
# SCL_PIN = 5

# Initialize I2C
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
time.sleep_ms(50)

# Scan for I2C devices
slaves = i2c.scan()
print(f"I2C devices found: {[hex(addr) for addr in slaves]}")

if LIDAR_ADDRESS not in slaves:
    print('Bus error: Please check LIDAR wiring')
    print('Expected device address: 0x{:02x}'.format(LIDAR_ADDRESS))
    print('\nTroubleshooting:')
    print('1. Check that pin 5 on TF-Luna is connected to GND (enables I2C mode)')
    print('2. Verify SDA is connected to GPIO{} (D4 on XIAO)'.format(SDA_PIN))
    print('3. Verify SCL is connected to GPIO{} (D5 on XIAO)'.format(SCL_PIN))
    print('4. Check power supply (VCC to 5V, GND to GND)')
    sys.exit()

# Initialize LIDAR
lidar = LIDAR(i2c, LIDAR_ADDRESS)
print(lidar.version())

# Set distance range limits
# Output only when between 20cm and 150cm (sensor supports up to 800cm)
lidar.set_min_max(20, 150)

# Set sampling frequency to 250Hz
lidar.set_frequency(250)

# Main loop - read distance continuously
print("Starting distance measurements...")
while True:
    distance = lidar.distance()
    print(f"Distance: {distance} cm")
    time.sleep_ms(100)  # Read every 100ms
