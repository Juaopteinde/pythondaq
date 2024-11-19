import pyvisa


def list_resources():
    """Retrieves and returns a list of connected resources.

    Returns:
        list: contains connected resources
    """
    rm = pyvisa.ResourceManager("@py")
    connected_ports = rm.list_resources()
    return connected_ports


class ArduinoVisaDevice:
    """Controls Arduino by sending direct commands using VISA.


    Attributes:
    port (str): port to which the arduino is connected


    Methods:
    get_identification()
    set_output_value(value)
    get_output_value()
    get_input_value(channel)
    get_input_voltage(channel)
    """

    def __init__(self, port):
        """Initialize the arduino and make it callable for the rest of the class.

        Args:
            port (str): port to which arduino is connected
        """
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

    def get_identification(self):
        """Identify the device connected to the port.

        Returns:
            str: identification string from connected device
        """
        identification = self.device.query("*IDN?")
        return identification

    def set_output_value(self, value):
        """Set ADC output value between 0 and 1023 on channel 0.

        Args:
            value (str): integer output voltage
        """
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        """Read output value on channel 0.

        Returns:
            str: ADC value outputted on channel 0
        """
        output_value = self.device.query("OUT:CH0?")
        return output_value

    def get_input_value(self, channel):
        """Measure inputted ADC value on given channel.

        Args:
            channel (str): channel you want to measure ADC voltage value on

        Returns:
            str: ADC value inputted on set channel
        """
        input_value = self.device.query(f"MEAS:CH{channel}?")
        return input_value

    def get_input_voltage(self, channel):
        """Meausre inputted voltage on given channel.

        Args:
            channel (str): channel you want to measure voltage on

        Returns:
            str: voltage inputted on set channel
        """
        step = 3.3 / 1023
        input_voltage = (int(self.device.query(f"MEAS:CH{channel}?"))) * step
        return input_voltage


if __name__ == "__main__":
    list_resources()
