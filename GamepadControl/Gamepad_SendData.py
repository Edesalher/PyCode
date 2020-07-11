import inputs
import time
import serial

pads = inputs.devices.gamepads
port = serial.Serial('COM6', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
time.sleep(2)

if len(pads) == 0:  #Se detecta si existe un Gampepad conectado o no.
    raise Exception("Couldn't find any Gamepads!")

while True:
    events = inputs.get_gamepad()
    for event in events:
        #print(event.ev_type, event.code, event.state)
        #BUTTONS
        if event.ev_type == 'Key':  #Se detecta si el evento es tipo "Key" --> Botones A,B,Y,X
            if event.state == 1:  #Se lee si el valor del botón es 1
                if event.code == 'BTN_SOUTH':
                    print("A")
                    port.write(b'A')
                elif event.code == 'BTN_EAST':
                    print("B")
                    port.write(b'B')
                elif event.code == 'BTN_NORTH':
                    print("Y")
                    port.write(b'Y')
                elif event.code == 'BTN_WEST':
                    print("X")
                    port.write(b'X')
            elif event.state == 0:  #Se lee si el valor del botón es 0
                print("Released")
                port.write(b'-')
        elif event.ev_type == 'Absolute':  #Se detecta si el evento es tipo "Absolute" -> Cruceta, gatillos, joysticks
            #CRUCETA
            if event.state == 1:  #Se lee si el valor del botón es 1
                if event.code == 'ABS_HAT0Y':
                    print("DOWN")
                elif event.code == 'ABS_HAT0X':
                    print("RIGHT")
            elif event.state == -1:  #Se lee si el valor del botón es -1
                if event.code == 'ABS_HAT0Y':
                    print("UP")
                elif event.code == 'ABS_HAT0X':
                    print("LEFT")
            elif event.state == 0:  #Se lee si el valor del botón es 0
                print("Released")
            #JOYSTICKS
            elif event.code == 'ABS_Y':  #Se detecta si el Joystick L se movío Arriba o Abajo.
                if event.state == 128:
                    print("Center R")
                elif event.state == 32767:
                    print("UP R")
                elif event.state == -32768:
                    print("DOWN R")
            elif event.code == 'ABS_X':  #Se detecta si el Joystick L se movío Derecha o Izuierda.
                if event.state == 128:
                    print("Center R")
                elif event.state == 32767:
                    print("RIGHT R")
                elif event.state == -32768:
                    print("LEFT R")