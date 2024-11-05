from arduino_device import ArduinoVisaDevice


class DiodeExperiment:

    # Initialize the arduino used by other methods
    def __init__(self, port):
        self.arduino = ArduinoVisaDevice(port)

    # Start a U, I, measurement of an LED by increasing U from start to stop
    # U is in ADC values (0 - 1023)
    def scan(self, start, stop, repeats):

        # Create lists to store measurements
        voltages_scan_LED = []
        currents_scan_LED = []

        # Perform the measurements
        for voltage in range(start, stop + 1):
            self.arduino.set_output_value(value=voltage)

            voltage_LED_list = []
            current_LED_list = []

            for repeat in range(0, repeats):
                voltage_resistor = float(self.arduino.get_input_voltage(channel=2))
                current = voltage_resistor / 220

                voltage_LED = (
                    float(self.arduino.get_input_voltage(channel=1)) - voltage_resistor
                )

                voltage_LED_list.append(voltage_LED)
                current_LED_list.append(current)

            print(voltage_LED_list)
            mean_voltage_LED = sum(voltage_LED_list) / repeats
            mean_current_LED = sum(current_LED_list) / repeats

            print(f"Voltage over the LED is {round(mean_voltage_LED, 3)} V")
            print(f"Current through the LED is {round(mean_current_LED, 6)} A")

            voltages_scan_LED.append(mean_voltage_LED)
            currents_scan_LED.append(mean_current_LED)

        # Turn off lamp after scan
        self.arduino.set_output_value(value=0)

        return voltages_scan_LED, currents_scan_LED
