from microdot import Microdot
from microdot.websocket import with_websocket
from microdot.cors import CORS
from machine import Pin, PWM
import asyncio 
import network
import time
from math import sin, cos

# to do list:
# make motors move
# have motors move in right directions
# put sufficient comments for each part of code

# Initialize PWM and direction pins
PWM1 = PWM(Pin(3, Pin.OUT), freq=1000)
PWM2 = PWM(Pin(11, Pin.OUT), freq=1000)
PWM3 = PWM(Pin(27, Pin.OUT), freq=1000)
PWM4 = PWM(Pin(19, Pin.OUT), freq=1000)
bL_pin1, bL_pin2 = Pin(0, Pin.OUT), Pin(10, Pin.OUT) # in1, in2 (motor1)
fL_pin1, fL_pin2 = Pin(9, Pin.OUT), Pin(5, Pin.OUT) # in3, in4 (motor2)
fR_pin1, fR_pin2 = Pin(26, Pin.OUT), Pin(22, Pin.OUT) # in5, in6 (motor3)
bR_pin1, bR_pin2 = Pin(20, Pin.OUT), Pin(21, Pin.OUT) # in7, in8 (motor4)

'''
en1, en2, en3, en4 = 3, 11, 27, 19
enable1 = machine.PWM(machine.Pin(en1))
enable1.freq(1000)
enable2 = machine.PWM(machine.Pin(en2))
enable2.freq(1000)
enable3 = machine.PWM(machine.Pin(en1))
enable3.freq(1000)
enable4 = machine.PWM(machine.Pin(en2))
enable4.freq(1000)
'''

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SBRT', 'Robotic$3')
time.sleep(5)

# Wait for connection
max_attempts = 10
attempt = 0

while not wlan.isconnected() and attempt < max_attempts:
    print(f"Trying to connect to (Attempt {attempt + 1}/{max_attempts})...")
    time.sleep(10)
    attempt += 1

if wlan.isconnected():
    print("Connected to IP:", wlan.ifconfig()[0])
else:
    print("Failed to connect to Wi-Fi. Please check your SSID and password.")

def motor_forward(speed, pin1, pin2, pwm):
    pin1.high()
    pin2.low()
    pwm.duty_u16(int(speed*65535))
def motor_reverse(speed, pin1, pin2, pwm):
    pin1.low()
    pin2.high()
    pwm.duty_u16(int(speed*65535))
def motor_stop(pin1, pin2, pwm):
    pin1.low()
    pin2.low()
    pwm.duty_u16(0)

# keep this:
app = Microdot()
CORS(app, allowed_origins = '*', allow_credentials = True)

@app.get('/test')
def index(requsst):
    return "hello world"

@app.get('/direction')
@with_websocket
async def index(request, ws):
    try:
        while True:
            mode = await ws.receive()
            ## Insert your logic here
            print("key", mode)
            #big robot
            '''
            if mode=='w':
                motor_forward(75, bL_pin1, bL_pin2, PWM1)
                motor_forward(75, fL_pin1, fL_pin2, PWM2)
                motor_forward(75, fR_pin1, fR_pin2, PWM3)
                motor_forward(75, bR_pin1, bR_pin2, PWM4)
            elif mode=='s':
                motor_reverse(75, bL_pin1, bL_pin2, PWM1)
                motor_reverse(75, fL_pin1, fL_pin2, PWM2)
                motor_reverse(75, fR_pin1, fR_pin2, PWM3)
                motor_reverse(75, bR_pin1, bR_pin2, PWM4)
            elif mode=='a':
                motor_reverse(75, bL_pin1, bL_pin2, PWM1)
                motor_reverse(75, fL_pin1, fL_pin2, PWM2)
                motor_forward(75, fR_pin1, fR_pin2, PWM3)
                motor_forward(75, bR_pin1, bR_pin2, PWM4)
            elif mode=='d':
                motor_forward(75, bL_pin1, bL_pin2, PWM1)
                motor_forward(75, fL_pin1, fL_pin2, PWM2)
                motor_reverse(75, fR_pin1, fR_pin2, PWM3)
                motor_reverse(75, bR_pin1, bR_pin2, PWM4)
            '''
                
            #small robot
            if mode=='w': #compared to a
                motor_reverse(75, bL_pin1, bL_pin2, PWM1) 
                motor_reverse(75, fL_pin1, fL_pin2, PWM2) 
                motor_forward(75, fR_pin1, fR_pin2, PWM3)
                motor_forward(75, bR_pin1, bR_pin2, PWM4)
            elif mode=='s': #compared to d
                motor_forward(75, bL_pin1, bL_pin2, PWM1)
                motor_forward(75, fL_pin1, fL_pin2, PWM2) 
                motor_reverse(75, fR_pin1, fR_pin2, PWM3)
                motor_reverse(75, bR_pin1, bR_pin2, PWM4)
            elif mode=='a': #compared to w
                motor_forward(75, bL_pin1, bL_pin2, PWM1)
                motor_forward(75, fL_pin1, fL_pin2, PWM2)
                motor_forward(75, fR_pin1, fR_pin2, PWM3)
                motor_forward(75, bR_pin1, bR_pin2, PWM4)
            elif mode=='d': #compared to s
                motor_reverse(75, bL_pin1, bL_pin2, PWM1)
                motor_reverse(75, fL_pin1, fL_pin2, PWM2)
                motor_reverse(75, fR_pin1, fR_pin2, PWM3)
                motor_reverse(75, bR_pin1, bR_pin2, PWM4)
            
            else:
                motor_stop(bL_pin1, bL_pin2, PWM1)
                motor_stop(fL_pin1, fL_pin2, PWM2)
                motor_stop(fR_pin1, fR_pin2, PWM3)
                motor_stop(bR_pin1, bR_pin2, PWM4)
                
            
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed")

app.run(port=80)
#testing vin
