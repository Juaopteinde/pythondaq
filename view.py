import matplotlib.pyplot as plt

from diode_experiment import DiodeExperiment

# Define port connected to arduino
port = "ASRL4::INSTR"

# Run measurements and save the data
measurement = DiodeExperiment(port)
voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = measurement.scan(
    0, 1023, 3
)

print(errors_currents_LED)
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
