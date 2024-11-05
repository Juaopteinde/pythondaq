from arduino_device import ArduinoVisaDevice


class DiodeExperiment:

    # Initialize the arduino used by other methods
    def __init__(self, port):
        self.arduino = ArduinoVisaDevice(port)

    # Start a U, I, measurement of an LED by increasing U from start to stop
    # U is in ADC values (0 - 1023)
    def scan(self, start, stop):

        # Create lists to store measurements
        voltages_scan_LED = []
        Currents_scan_LED = []

        # Perform the measurements
        for voltage in range(start, stop + 1):
            self.arduino.set_output_value(value=voltage)

            voltage_resistor = float(self.arduino.get_input_voltage(channel=2))
            current = voltage_resistor / 220

            voltage_LED = (
                float(self.arduino.get_input_voltage(channel=1)) - voltage_resistor
            )

            print(f"Voltage over the LED is {voltage_LED} V")
            print(f"Current through the LED is {current} A")

            voltages_scan_LED.append(voltage_LED)
            Currents_scan_LED.append(current)

        return voltages_scan_LED, Currents_scan_LED
