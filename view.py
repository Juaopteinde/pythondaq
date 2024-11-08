import matplotlib.pyplot as plt

from diode_experiment import DiodeExperiment

# Define port connected to arduino
port = "ASRL4::INSTR"

start, stop = input(
    "In what range do you want to scan? Give start and stop value seperated by a space. e.g. 800 900 \n"
).split()

repeats = input("How many times do you want to repeat the measurement? \n")

# Run measurements and save the data
measurement = DiodeExperiment(port)
voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = measurement.scan(
    int(start), int(stop), 3  # start stop repeats
)

# Plot the data
plt.errorbar(
    voltages_LED,
    currents_LED,
    xerr=errors_voltages_LED,
    yerr=errors_currents_LED,
    ecolor="red",
    fmt="o",
    markersize=4,
)
plt.title("I-U diagram of LED")
plt.xlabel("Voltage U (V)")
plt.ylabel("Current I (Amp)")
plt.show()
