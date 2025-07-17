from naoqi import ALProxy
import sys

# Replace this with your robot's IP address
ROBOT_IP = "127.168.1.100"
PORT = 9559

def main():
    try:
        # Create proxies
        motion = ALProxy("ALMotion", ROBOT_IP, PORT)
        posture = ALProxy("ALRobotPosture", ROBOT_IP, PORT)

        # Wake up the robot
        motion.wakeUp()

        # Go to Stand posture
        print("Sending robot to Stand posture...")
        posture.goToPosture("Sit", .50)
        print("Robot is now standing.")

    except Exception as e:
        print("[ERROR]", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

