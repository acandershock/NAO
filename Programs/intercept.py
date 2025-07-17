from naoqi import ALProxy, ALModule, ALBroker
import sys
import time

# Global reference to the module instance
global_touch_interceptor = None

# Top-level event handler function (NAOqi requires this)
def onTouchHandler(eventName, value, subscriberIdentifier):
    global global_touch_interceptor
    if global_touch_interceptor:
        global_touch_interceptor.on_touch(eventName, value, subscriberIdentifier)

# Custom module class
class TouchInterceptor(ALModule):
    def __init__(self, name, broker, robot_ip, port):
        ALModule.__init__(self, name)
        self.name = name
        self.mem = ALProxy("ALMemory", robot_ip, port)

        self.events = [
            "FrontTactilTouched",
            "MiddleTactilTouched",
            "RearTactilTouched",
            "LeftBumperPressed",
            "RightBumperPressed"
        ]

        print("Setting up event interception...")

        # Unsubscribe default behavior tree subscribers
        for event in self.events:
            try:
                subscribers = self.mem.getSubscribers(event)
                for sub in subscribers:
                    if sub != self.name:
                        try:
                            self.mem.unsubscribeToEvent(event, sub)
                            print("Unsubscribed {} from {}".format(sub, event))
                        except Exception as e:
                            print("Could not unsubscribe {} from {}: {}".format(sub, event, e))
            except Exception as e:
                print("Could not get subscribers for {}: {}".format(event, e))

        # Subscribe this module using top-level handler
        for event in self.events:
            try:
                self.mem.subscribeToEvent(event, self.name, "onTouchHandler")
                print("Subscribed {} to {}".format(self.name, event))
            except Exception as e:
                print("Could not subscribe {} to {}: {}".format(self.name, event, e))

    def on_touch(self, eventName, value, subscriberIdentifier):
        if value == 1.0:
            print("\nEvent Triggered: {}".format(eventName))
            print("Value: {}".format(value))
        elif value == 0.0:
            print("Released: {}".format(eventName))

# Main execution
if __name__ == "__main__":
    ROBOT_IP = "127.0.0.1"  # running locally on NAO
    PORT = 9559
    MODULE_NAME = "TouchInterceptor"

    # Start the broker
    broker = ALBroker("myBroker",
                      "0.0.0.0",  # Listen on all interfaces
                      0,          # Use random available port
                      ROBOT_IP,
                      PORT)

    # Create and store the module globally
    global_touch_interceptor = TouchInterceptor(MODULE_NAME, broker, ROBOT_IP, PORT)

    print("\nTouchInterceptor is now running. Press Ctrl+C to exit.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user, shutting down.")
        broker.shutdown()
        sys.exit(0)

