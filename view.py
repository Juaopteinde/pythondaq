import matplotlib.pyplot as plt

from diode_experiment import DiodeExperiment

# Define port connected to arduino
port = "ASRL4::INSTR"

# Run measurements and save the data
measurement = DiodeExperiment(port)
voltages_LED, currents_LED = measurement.scan(0, 1024)

# Plot the data
plt.plot(voltages_LED, currents_LED, "o")
plt.title("I-U diagram of LED")
plt.xlabel("Voltage U (V)")
plt.ylabel("Current I (Amp)")
plt.show()
