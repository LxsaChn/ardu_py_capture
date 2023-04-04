import time as utime
import busio
import board
import usb_cdc
from Arducam import *
from board import *
import time


mode = 0
start_capture = 0
stop_flag=0
once_number=128
value_command=0
flag_command=0
buffer=bytearray(once_number)

mycam = ArducamClass(OV5642)
mycam.Camera_Detection()
mycam.Spi_Test()
mycam.Camera_Init()
mycam.Spi_write(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)
utime.sleep(1)
mycam.clear_fifo_flag()
mycam.Spi_write(ARDUCHIP_FRAMES,0x00)

def read_fifo_burst():
    count=0
    lenght=mycam.read_fifo_length()
    mycam.SPI_CS_LOW()
    mycam.set_fifo_burst()
    while True:
        mycam.spi.readinto(buffer,start=0,end=once_number)
        usb_cdc.data.write(buffer)
        utime.sleep(0.00015)
        count+=once_number
        if count+once_number>lenght:
            count=lenght-count
            mycam.spi.readinto(buffer,start=0,end=count)
            usb_cdc.data.write(buffer)
            mycam.SPI_CS_HIGH()
            mycam.clear_fifo_flag()
            break

while True:   
    mycam.flush_fifo()
    mycam.clear_fifo_flag()
    mycam.OV5642_set_JPEG_size(OV5642_2048x1536)

    mycam.start_capture()
    read_fifo_burst()
    mycam.clear_fifo_flag()
    time.sleep(10)

