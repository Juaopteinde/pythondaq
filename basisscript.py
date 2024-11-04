import csv
import os

import matplotlib.pyplot as plt
import pyvisa
from arduino_device import ArduinoVisaDevice, list_resources

# Get available ports
list_resources()

# Call on the class using the right port
port = xxx
arduino = ArduinoVisaDevice(port)

# Create lists for the voltage and current through the LED
U_list_LED = []
I_list_LED = []

# Up the current from min to max, measure and calculate voltages & current
for voltage in range(0, 1024):

    # Change output voltage, in ADC values (0 - 1023)
    arduino.set_output_value(value=voltage)

    # Measure voltages over resistor & LED
    voltage_resistor = int(arduino.get_input_voltage(channel=2))
    voltage_LED = int(arduino.get_input_voltage(channel=1)) - int(
        arduino.get_input_voltage(channel=2)
    )

    # Calculate current for 220 Ohm resistor
    current = voltage_resistor / 220

    # Append voltage and current to their corresponding lists
    U_list_LED.append(voltage_LED)
    I_list_LED.append(current)

    print(f"Outgoing voltage = {arduino.get_output_value()}")
    print(f"Raw value voltage over LED is {voltage_LED}. Voltage is {voltage_LED}.")
    print(
        f"Raw value voltage over resistor is {voltage_resistor}. Voltage is {voltage_resistor}."
    )


# Turn off LED after measurements
arduino.set_output_value(value=0)

plt.plot(
    U_list_LED,
    I_list_LED,
)
plt.title("I-U diagram of LED")
plt.xlabel("Voltage U (V)")
plt.ylabel("Current I (Amp)")
plt.show()

# Create a list of all files in the current directory
current_directory = os.getcwd()
entries = os.listdir(current_directory)

# Check if the current filename already exists in the current directory, if not create a new filename
filename = "metingen_0.csv"
counter = 0
while filename in entries:
    filename = f"metingen_{counter}.csv"
    counter += 1

# Create file with the new filename
with open(f"{filename}", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["I", "U"])
    for I_list_LED, U_list_LED in zip(I_list_LED, U_list_LED):
        writer.writerow([I_list_LED, U_list_LED])
