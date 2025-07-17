from naoqi import ALProxy
import time

# Configuration
IP = "127.0.0.1"  # Replace with your NAO's IP address
PORT = 9559

# Events to monitor
TOUCH_EVENTS = [
    "FrontTactilTouched",
    "MiddleTactilTouched",
    "RearTactilTouched",
    "LeftBumperPressed",
    "RightBumperPressed"
]

# Set up proxy
try:
    mem = ALProxy("ALMemory", IP, PORT)
except Exception as e:
    print("Could not create ALMemory proxy:", e)
    exit(1)

# Keep a record of what we've already reported
last_values = {event: 0.0 for event in TOUCH_EVENTS}

print("Listening for touch events. Touch the robot to trigger tracing...\n")

try:
    while True:
        for event in TOUCH_EVENTS:
            try:
                value = mem.getData(event)

                # Trigger only on change from 0.0 to 1.0
                if value == 1.0 and last_values[event] != 1.0:
                        print("\nEvent Triggered: {}".format(event))
                        print("Value: {}".format(value))
    
                        subscribers = mem.getSubscribers(event)
                        print("Subscribers to '{}' event:".format(event))
                        for sub in subscribers:
                                print(" - {}".format(sub))
                        print()

                last_values[event] = value
            except Exception as e:
                print("Error reading {}: {}".format(event, e))
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped by user")
