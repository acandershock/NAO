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

        stiffnesses = 0.0
        motion.setStiffnesses("Body", stiffnesses)

    except Exception as e:
        print("[ERROR]", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

