class Serial:

    import serial

    portName = "/dev/ttyACM0"
    baudRate = 9600
    ser = serial.Serial(portName, baudRate, timeout=1)

    ser.flushInput()
    ser.flushOutput()



    ser.write(1)
