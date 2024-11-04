from arduino_device import ArduinoVISADevice, list_resources


class DiodeExperiment:

    # Initialize the arduino used by other methods
    def __init__(self, port):
        self.arduino = ArduinoVISADevice(port)

    # Start a U, I, measurement of an LED by increasing U from start to stop
    # U is in ADC values (0 - 1023)
    def scan(self, start, stop):

        # Create lists to store measurements
        Voltages_scan_LED = []
        Currents_scan_LED = []

        # Perform the measurements
        for voltage in range(start, stop + 1):
            self.arduino.query(f"OUT:CH0 {voltage}")

            voltage_resistor = int(self.arduino.get_input_voltage(channel=2))
            current = voltage_resistor / 220

            voltage_LED = (
                int(self.arduino.get_input_voltage(channel=1)) - voltage_resistor
            )

            Voltages_scan_LED.append(voltage_LED)
            Currents_scan_LED.append(current)

        return voltage_LED, Currents_scan_LED
