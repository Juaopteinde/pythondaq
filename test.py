from arduino_device import ArduinoVisaDevice

device = ArduinoVisaDevice("ASRL4::INSTR")

print(device.get_identification())
