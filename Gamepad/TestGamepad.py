import inputs

pads = inputs.devices.gamepads

if len(pads) == 0:
    raise Exception("Couldn't find any Gamepads!")

while True:
    events = inputs.get_gamepad()
    for event in events:
        #print(event.ev_type)
        #print(event.code)
        #print(event.state)
        print(event.ev_type, event.code, event.state)
        #if event.code == 'BTN_SOUTH' and event.state == 1:
         #   print("You've press button: A")
        #else:
         #   print("Button A has been released")