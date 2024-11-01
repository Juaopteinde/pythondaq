import csv
import os

import matplotlib.pyplot as plt
import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
device = rm.open_resource(
    "ASRL4::INSTR", read_termination="\r\n", write_termination="\n"
)
identification = device.query("*IDN?")


# Convert raw 10 bit value to volt
def raw_value_to_volt(raw_value):
    step = 3.3 / 1023
    volt = raw_value * step
    return volt


# Convert volt to 10 bit value
def volt_to_raw_value(volt):
    step = 1023 / 3.3
    raw_value = step * volt
    return raw_value


# Create lists for the voltage and current through the LED
U_list_LED = []
I_list_LED = []

# Up the current from min to max, measure and calculate voltages & current
for voltage in range(0, 1024):

    # Change outgoing voltage
    device.query(f"OUT:CH0 {voltage}")

    # Measure voltages over resistor & LED
    raw_value_resistor = int(device.query("MEAS:CH2?"))
    raw_value_LED = int(device.query("MEAS:CH1?")) - int(device.query("MEAS:CH2?"))

    # Convert raw values to volt
    voltage_LED = raw_value_to_volt(raw_value_LED)
    voltage_resistor = raw_value_to_volt(raw_value_resistor)

    # Calculate current for 220 Ohm resistor
    current = voltage_resistor / 220

    # Append voltage and current to their corresponding lists
    U_list_LED.append(voltage_LED)
    I_list_LED.append(current)

    print(
        f"Outgoing voltage = {raw_value_to_volt(int(device.query("OUT:CH0?")))}, raw value = {device.query("OUT:CH0?")}"
    )
    print(f"Raw value voltage over LED is {raw_value_LED}. Voltage is {voltage_LED}.")
    print(
        f"Raw value voltage over resistor is {raw_value_resistor}. Voltage is {voltage_resistor}."
    )


# Turn off LED after measurements
device.query("OUT:CH0 0")

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
