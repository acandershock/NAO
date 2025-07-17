from naoqi import ALProxy

robot_ip = "127.0.0.1"
port = 9559

mem = ALProxy("ALMemory", robot_ip, port)

events = [
    "FrontTactilTouched",
    "MiddleTactilTouched",
    "RearTactilTouched",
    "LeftBumperPressed",
    "RightBumperPressed"
]

for event in events:
    try:
        subs = mem.getSubscribers(event)
        print("Subscribers for '{}': {}".format(event, subs))
    except Exception as e:
        print("Error getting subscribers for {}: {}".format(event, e))
