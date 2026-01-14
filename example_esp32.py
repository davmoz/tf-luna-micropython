"""
TF-Luna LiDAR Example for ESP32 Boards

Pin Configuration for ESP32:
- Default I2C pins: SDA=GPIO21, SCL=GPIO22
- You can use any GPIO pins that support I2C

Wiring for TF-Luna:
1. VCC  -> 5V (or 3.3V)
2. RXD/SDA -> Connect to SDA pin (default GPIO21)
3. TXD/SCL -> Connect to SCL pin (default GPIO22)
4. GND  -> GND
5. Configuration Input -> GND (to enable I2C mode)
"""

from machine import I2C, Pin
import time
import sys
from lib.lidar import LIDAR

# TF-Luna has the default slave_address 0x10
LIDAR_ADDRESS = 0x10

# Configure I2C pins for ESP32
# Using default ESP32 I2C pins
SDA_PIN = 21  # Default SDA pin on ESP32
SCL_PIN = 22  # Default SCL pin on ESP32

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
    print('2. Verify SDA is connected to GPIO{}'.format(SDA_PIN))
    print('3. Verify SCL is connected to GPIO{}'.format(SCL_PIN))
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
