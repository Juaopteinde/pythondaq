import numpy as np

from pythondaq.arduino_device import ArduinoVisaDevice


class DiodeExperiment:
    """Run voltage and current measurement on Arduino.

    Attributes:
    port (str): port connected to arduino

    Methods:
    scan(start, stop, repeats)
    """

    # Initialize the arduino used by other methods
    def __init__(self, port):
        """Open connection to arduino through class ArduinoVisaDevice.

        Args:
            port (str): port connected to arduino
        """
        self.arduino = ArduinoVisaDevice(port)

    def scan(self, start, stop, repeats):
        """Run a U-I measurement on a LED by increasing the ADC OUTPUT voltage and measuring ADC INPUT voltage.

        Args:
            start (int): starting ADC voltage value
            stop int): stopping ADC voltage value
            repeats (int): amount of measurements per ADC voltage value

        Returns:
            list: measurement data, including measured voltage, current, and errors on voltage and current
        """

        # Create lists to store measurements
        voltages_scan_LED = []
        currents_scan_LED = []
        sem_voltage_LED_list = []
        sem_current_LED_list = []

        # Perform the measurements
        print("Starting scan")
        for voltage in range(start, stop + 1):

            # Set OUTPUT voltage
            self.arduino.set_output_value(value=voltage)

            voltage_LED_list = []
            current_LED_list = []

            # Perform repeated measurements for the same voltage
            for repeat in range(0, repeats):
                voltage_resistor = float(self.arduino.get_input_voltage(channel=2))
                current = voltage_resistor / 220

                voltage_LED = (
                    float(self.arduino.get_input_voltage(channel=1)) - voltage_resistor
                )

                voltage_LED_list.append(voltage_LED)
                current_LED_list.append(current)

            # Convert to numpy arrays for efficiency
            voltage_LED_array = np.array(voltage_LED_list)
            current_LED_array = np.array(current_LED_list)

            # Calculate mean of repeated measurement
            mean_voltage_LED = np.mean(voltage_LED_array)
            mean_current_LED = np.mean(current_LED_array)

            voltages_scan_LED.append(float(mean_voltage_LED))
            currents_scan_LED.append(float(mean_current_LED))

            # Calculate standarddeviation of repeated measurement
            sigma_voltage_LED = np.std(voltage_LED_array)
            sigma_current_LED = np.std(current_LED_array)

            # Calculate standard error of means of repeated measurement
            sem_voltage_LED = sigma_voltage_LED / np.sqrt(repeats)
            sem_current_LED = sigma_current_LED / np.sqrt(repeats)

            sem_voltage_LED_list.append(float(sem_voltage_LED))
            sem_current_LED_list.append(float(sem_current_LED))

        # Turn off lamp after scan
        self.arduino.set_output_value(value=0)

        return (
            voltages_scan_LED,
            currents_scan_LED,
            sem_voltage_LED_list,
            sem_current_LED_list,
        )
