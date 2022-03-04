import time
from datetime import datetime
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import json
import random
import json
import csv
import os
# Import the RFM9x radio module.
import adafruit_rfm9x
# Import lcd driver
import drivers

#-----------------------------------------------------------
# def var
basiccycle = 0.2
countcycle = 0
cycle1s = 5 # 5 lan basiccycle
cycle10s = 50
cycle20s = 100
cycle1m = 300
data_size = 450
count = 0
text_index = 0
#latitude=0
#longitude=0
#speed=0
#fuel=0
#status=0
send_data={}

#-----------------------------------------------------------
# def function
def LoRaReceive():
    packet = None  
    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:        
        #print('- Waiting for PKT -')
        pass
    else:
        # Display the packet text and rssi        
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print('RX: ')
        print(packet_text)
        
def LoRaSend():
    global send_data
    global text_index
    send_json=json.dumps(send_data)       
    send_byte = bytes(send_json, "utf-8")
    rfm9x.send(send_byte)
    print(send_json)
    text_index=0
    #long_string(display, send_json, 2)

def ButtonClick():
    global btnA
    global btnB
    global btnC
    if not btnA.value:
        # Send Button A        
        #button_a_data = bytes("Button A!", "utf-8")
        #rfm9x.send(button_a_data)
        print('shutdown now!')
        display.lcd_clear()
        time.sleep(1)
        os.system("sudo shutdown now")
    elif not btnB.value:
        # Send Button B
        button_b_data = bytes("Button B!", "utf-8")
        rfm9x.send(button_b_data)
        print('Sent Button B!')        
    elif not btnC.value:
        # Send Button C        
        #button_c_data = bytes("Button C!", "utf-8")
        #rfm9x.send(button_c_data)
        #print('Sent Button C!')
        os.system("shutdown now")
        
def ButtonInit():
    global btnA
    global btnB
    global btnC
    # Button A
    btnA = DigitalInOut(board.D5)
    btnA.direction = Direction.INPUT
    btnA.pull = Pull.UP

    # Button B
    btnB = DigitalInOut(board.D6)
    btnB.direction = Direction.INPUT
    btnB.pull = Pull.UP

    # Button C
    btnC = DigitalInOut(board.D12)
    btnC.direction = Direction.INPUT
    btnC.pull = Pull.UP
        
def ReadCsv():
    global count
    global send_data
    global l
    # read gps data from dataset
    latitude = float(l[count+1][7])
    longitude = float(l[count+1][6])
    speed = float(l[count+1][8])
    fuel = count%10000
    status = "On route"    
    send_data = {
        "latitude":round(latitude,3),
        "longitude":round(longitude,3),
        "speed":round(speed,2),
        "fuel":fuel,
        "status":status
        }
    count = (count+1)%data_size
    
def long_string(display, text='', num_line=2, num_cols=16):
    """ 
    Parameters: (driver, string to print, number of line to print, number of columns of your display)
    Return: This function send to display your scrolling string.
    """
    if len(text) > num_cols:
        display.lcd_display_string(text[:num_cols], num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print, num_line)            
            time.sleep(0.2)
        time.sleep(1)
    else:
        display.lcd_display_string(text, num_line)
def long_string_new(display, text='', num_line=2, num_cols=16):
    """ 
    Parameters: (driver, string to print, number of line to print, number of columns of your display)
    Return: This function send to display your scrolling string.
    """
    global text_index
    if len(text) > num_cols:
        text_to_print = text[text_index:text_index+num_cols]
        display.lcd_display_string(text_to_print, num_line)
        if (text_index<(len(text) - num_cols + 1)):
            text_index = (text_index+1)             
    else:
        display.lcd_display_string(text, num_line)

#-----------------------------------------------------------
# setup par
# read dataset from csv file
with open('/home/pi/DCLV/data/data_gps.csv') as f:
    reader = csv.reader( f)
    l = [row for row in reader]

# Button Init
ButtonInit()

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.D25)
RESET = DigitalInOut(board.D17)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)
rfm9x.tx_power = 23
prev_packet = None

# setup timer
starttime = time.time()


# setup Lcd
display = drivers.Lcd()
display.lcd_display_string("Stetup finish!", 1)
print("Stetup finish!")

#-----------------------------------------------------------
# main loop
try:
    while True:
        # basiccycle
        #LoRaReceive()
        ButtonClick()
        long_string_new(display, json.dumps(send_data), 2)
        if ((countcycle%cycle1s)==0):
            # cycle 1s
            display.lcd_display_string(str(datetime.now().time()), 1)
            #print("cycle1s")
        if ((countcycle%cycle10s)==0):
            # cycle 10s
            #ReadCsv()
            #LoRaSend()
            pass
            #print("cycle10s")
        if ((countcycle%cycle20s)==0):
            # cycle 20s
            ReadCsv()
            LoRaSend()
            #print("cycle20s")
        if ((countcycle%cycle1m)==0):
            # cycle 1m
            pass
            #print("cycle1m")      
                
                
        countcycle=countcycle+1
        #print(basiccycle-((time.time()-starttime)%basiccycle))
        time.sleep(basiccycle-((time.time()-starttime)%basiccycle))
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Exit program!")
    display.lcd_clear()


