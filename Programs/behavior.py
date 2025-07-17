from naoqi import ALProxy

robot_ip = "127.0.0.1"  # or your robot's IP
port = 9559

behavior_manager = ALProxy("ALBehaviorManager", robot_ip, port)

# List running behaviors
running_behaviors = behavior_manager.getRunningBehaviors()
print("Currently running behaviors:", running_behaviors)
