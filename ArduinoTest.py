from ArduinoDigital import ArduinoDigital

##### main
opcode = -1
arduino = ArduinoDigital("COM7")

while opcode != 0:
    opcodestr = input("opcode [0- exit, 1- Valve on, 2- Valve of]: ")
    opcode = int(opcodestr)

    if opcode == 0:
        print("Program terminated")

    elif opcode == 1:
        pin = int(input("select valve: "))
        arduino.DigitalHigh(pin)

    elif opcode == 2:
        pin = int(input("select valve: "))
        arduino.DigitalLow(pin)

    else:
        print ("illegal opcode")
