import pyvisa


# Print list of connected ports
def list_resources():
    rm = pyvisa.ResourceManager("@py")
    print(rm.list_resources())


# Sends commands directly to arduino
# Can set OUTPUT voltage, and read INPUT voltages
class ArduinoVisaDevice:

    # Define the device used by the rest of the class
    def __init__(self, port):
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

    # Return identification string of the device connected to the given port
    def get_identification(self):
        identification = self.device.query("*IDN?")
        print("lmao")
        return identification

    # Set voltage on channel 0, in ADC values (0 - 1023)
    def set_output_value(self, value):
        self.device.query(f"OUT:CH0 {value}")
        print(f"Set ADC OUTPUT voltage on channel 0 to {value}")

    # Read and return the voltage on channel 0, in ADC values (0 - 1023)
    def get_output_value(self):
        output_value = self.device.query("OUT:CH0?")
        return output_value

    # Read and return the voltage on the given channel, in ADC values (0 - 1023)
    def get_input_value(self, channel):
        input_value = self.device.query(f"MEAS:CH{channel}?")
        return input_value

    # Read and return the voltage on the given channel, in voltage (0 - 3.3 V)
    def get_input_voltage(self, channel):
        step = 3.3 / 1023
        input_voltage = (float(self.device.query(f"MEAS:CH{channel}?"))) * step
        return input_voltage


# Print list of connected ports when this script is run directly
if __name__ == "__main__":
    list_resources()
