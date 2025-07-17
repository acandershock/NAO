from naoqi import ALProxy

tele = ALProxy("ALTelepathe", "127.0.0.1", 9559)
print(tele.getMethodList())
help(tele)
