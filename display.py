import smbus2
from PIL import Image

ADDRESS = 0b0100000 # Last 3 bits are the address
bus = smbus2.SMBus(1)

BIT_RS  = 0
BIT_E   = 1
BIT_CS1 = 2
BIT_CS2 = 3
BIT_RST = 4

IODIRA = 0x00
IODIRB = 0x01
GPIOA  = 0x12
GPIOB  = 0x13

LEFT  = 0
RIGHT = 1

#SECTION - Initialize State
STATE_INIT = (1 << BIT_CS1) | (1 << BIT_CS2) | (1 << BIT_RST)
state = STATE_INIT

#SECTION - Functions
def set_bit(bit):
    global state
    if (state >> bit) & 1 == 0:
        state = state | (1 << bit)
        bus.write_byte_data(ADDRESS, GPIOB, state)

def clear_bit(bit):
    global state
    if (state >> bit) & 1 == 1:
        state = state & ~(1 << bit)
        bus.write_byte_data(ADDRESS, GPIOB, state)

def _write_byte(byte, rs):
    if rs:
        set_bit(BIT_RS)
    else:
        clear_bit(BIT_RS)
    bus.write_byte_data(ADDRESS, GPIOA, byte)
    set_bit(BIT_E)
    clear_bit(BIT_E)

def send_instruction(byte):
    _write_byte(byte, 0)

def send_data(byte):
    _write_byte(byte, 1)

def select_chip(chip):
    if chip == LEFT:
        set_bit(BIT_CS2)
        clear_bit(BIT_CS1)
    elif chip == RIGHT:
        clear_bit(BIT_CS2)
        set_bit(BIT_CS1)
    else:
        raise ValueError("Invalid chip selection")

def reset_display():
    clear_bit(BIT_RST)
    set_bit(BIT_RST)

def init():
    bus.write_byte_data(ADDRESS, IODIRA, 0x00) # Set all A pins as output
    bus.write_byte_data(ADDRESS, IODIRB, 0x00) # Set all B pins as output
    
    bus.write_byte_data(ADDRESS, GPIOB, state)
    
    reset_display()
    
    for chip in [LEFT, RIGHT]:
        select_chip(chip)
        
        send_instruction(0x3F)  # Display ON
        send_instruction(0xC0)  # Set start line to 0
        send_instruction(0x40)  # Set Y address to 0
        send_instruction(0xB8)  # Set X address to 0
        
def write_screen(image):
    for chip in [LEFT, RIGHT]:
        select_chip(chip)
        x_offset = 0 if chip == LEFT else 64
        for page in range(8):
            send_instruction(0xB8 | page)
            #send_instruction(0x40 | 0)
            for col in range(64):
                x = x_offset + col
                byte = 0
                for bit in range(8):
                    y = page * 8 + bit
                    if image.getpixel((x, y)):
                        byte |= (1 << bit)
                byte = ~byte & 0xFF
                send_data(byte)
        
def clear_screen():
    write_screen(Image.new('1', (128, 64), 1))
