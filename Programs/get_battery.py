from naoqi import ALProxy

IP = "127.0.0.1"
PORT = 9559

def battery():
        memory = ALProxy("ALMemory", IP, PORT)

        all_keys = memory.getDataList("Device/SubDeviceList/Battery/")
        for key in all_keys:
                print(key)

def battery_status():
        mem = ALProxy("ALMemory", IP, PORT)
        values = [
                "Device/SubDeviceList/Battery/Charge/Sensor/Value",
                "Device/SubDeviceList/Battery/Charge/Sensor/RemainingCapacity",
                "Device/SubDeviceList/Battery/Charge/Sensor/FullChargeCapacity",
                "Device/SubDeviceList/Battery/Charge/Sensor/Status",
                "Device/SubDeviceList/Battery/Charge/Sensor/Age",
                "Device/SubDeviceList/Battery/Temperature/Sensor/Value",
                "Device/SubDeviceList/Battery/Temperature/Sensor/AmbientTemperature",
                "Device/SubDeviceList/Battery/Current/Sensor/Value"
        ]

        for val in values:
               status = mem.getData(val)
               print(" {}: {:.4f}".format(val, status))
        print("") 
        


if __name__ == "__main__":
        battery_status()
