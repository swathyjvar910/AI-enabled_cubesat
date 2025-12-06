# telemetry.py
import struct
import time
import random
import os

# Telmetry fields:
# - timestamp (unsigned int)
# # - battery_voltage (float)
# # - temperature (float)
# # - cpu_load (float)
# # - gyro_x (float)
# # - gyro_y (float)
# # - gyro_z (float)
# # - mode (unsigned char)
#
# # I = unsigned int (4 bytes)
# # 6f = 6 floats (24 bytes)
# # B = unsigned char (1 byte)
# # Total = 4 + 24 + 1 = 29 bytes per packet

packet_format = "I6fB"  # adjustable based on fields
packet_size = struct.calcsize(packet_format)
bin_file = "telemetry.bin"

# Modes of readability
mode_idle = 0
mode_science = 1
mode_safe = 2

def generate_telemetry_packet():
    """Generate one random CubeSat telemetry packet"""
    timestamp = int(time.time())
    battery_voltage = random.uniform(6.5, 8.4)  # volts
    temperature = random.uniform(-10, 60)   # Celsius
    cpu_load = random.uniform(0, 100)   # %
    gyro_x = random.uniform(-1, 1)
    gyro_y = random.uniform(-1, 1)
    gyro_z = random.uniform(-1, 1)

    mode = random.choice([mode_idle, mode_science, mode_safe])

    packet = struct.pack(
        packet_format,
        timestamp,
        battery_voltage,
        temperature,
        cpu_load,
        gyro_x,
        gyro_y,
        gyro_z,
        mode
    )
    return packet
def append_packet():
    """Generate one packet and append it to the binary file"""
    packet = generate_telemetry_packet()
    with open(bin_file, "ab") as f:
        f.write(packet)

def read_all_packets():
    """Read all telemetry packets from the binary file.
       Returns a list of tuples."""
    if not os.path.exists(bin_file):
        return []
    packets = []
    with open(bin_file, "rb") as f:
        while True:
            chunk = f.read(packet_size)
            if not chunk or len(chunk) < packet_size:
                break
            unpacked = struct.unpack(packet_format, chunk)
            packets.append(unpacked)
    return packets