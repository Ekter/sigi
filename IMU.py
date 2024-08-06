import smbus
import struct
import collections
import time

class Regs:
    CTRL1_XL = 0x10
    CTRL2_G = 0x11
    CTRL3_C = 0x12
    OUTX_L_G = 0x22
    OUTX_L_XL = 0x28

Vector = collections.namedtuple('Vector', 'x y z')

class LSM6:
    def __init__(self, slave_addr=0x6B):    # Use 0x6A or 0x6B depending on SDO/SA0 connection
        self.bus = smbus.SMBus(1)
        self.sa = slave_addr
        self.g = Vector(0, 0, 0)
        self.a = Vector(0, 0, 0)

    def enable(self):
        self.bus.write_byte_data(self.sa, Regs.CTRL1_XL, 0x50) # 208 Hz ODR, 2 g FS
        self.bus.write_byte_data(self.sa, Regs.CTRL2_G, 0x58) # 208 Hz ODR, 1000 dps FS
        self.bus.write_byte_data(self.sa, Regs.CTRL3_C, 0x04) # IF_INC = 1 (automatically increment register address)
        time.sleep(0.001)

    def read_gyro(self):
        byte_list = self.bus.read_i2c_block_data(self.sa, Regs.OUTX_L_G, 6)
        self.g = Vector(*struct.unpack('hhh', bytes(byte_list)))
        time.sleep(0.001)

    def read_accel(self):
        byte_list = self.bus.read_i2c_block_data(self.sa, Regs.OUTX_L_XL, 6)
        self.a = Vector(*struct.unpack('hhh', bytes(byte_list)))
        time.sleep(0.001)

    def read(self):
        self.read_gyro()
        self.read_accel()

