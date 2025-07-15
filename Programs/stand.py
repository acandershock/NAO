from naoqi import ALProxy
import time

# Target angles for standing-like posture (in radians)
LEG_JOINTS = {
  "LHipPitch": -0.5,
  "RHipPitch": -0.5,
  "LKneePitch": 1.0,
  "RKneePitch": 1.0,
  "LAnklePitch": -0.5,
  "RAnklePitch": -0.5,
  "LHipRoll": 0.0,
  "RHipRoll": 0.0
}

def read_joint_currents(mem, joints):
  print("\nJoint Motor Currents (Amps):")
  for joint in joints:
    key = "Device/SubDeviceList/{}/ElectricCurrent/Sensor/Value".format(joint)
    try:
      current = mem.getData(key)
      print("  {}: {:.4f} A".format(joint, current))
    except:
      print("  {}: ERROR reading current.".format(joint))
  print("")

def manual_stand_with_monitoring():
  motion = ALProxy("ALMotion", "127.0.0.1", 9559)
  mem = ALProxy("ALMemory", "127.0.0.1", 9559)

  joint_names = list(LEG_JOINTS.keys())
  target_angles = [LEG_JOINTS[j] for j in joint_names]

  # Step 1: Wake up and set stiffness
  print("Waking up robot...")
  motion.wakeUp()
  motion.setStiffnesses("Body", 0.5)
  time.sleep(1)

  # Step 2: Monitor currents before movement
  print("Reading joint currents before movement...")
  read_joint_currents(mem, joint_names)

  # Step 3: Move to standing-like posture
  print("Moving joints to stand-like posture...")
  motion.angleInterpolation(joint_names, target_angles, 3.0, True)

  # Step 4: Monitor currents after movement
  print("Reading joint currents after movement...")
  read_joint_currents(mem, joint_names)

  # Optional pause
  print("Holding posture for 3 seconds...")
  time.sleep(3)

  # Step 5: Relax
  print("Disabling stiffness...")
  motion.setStiffnesses("Body", 0.0)

  print("Manual stand-up sequence completed.")

if __name__ == "__main__":
  manual_stand_with_monitoring()
  
