import matplotlib.pyplot as plt

from diode_experiment import DiodeExperiment

port = "ASRL4::INSTR"
measurement = DiodeExperiment(port)
voltages_LED, currents_LED = measurement.scan(0, 1024)
plt.plot(voltages_LED, currents_LED, "o")
plt.title("I-U diagram of LED")
plt.xlabel("Voltage U (V)")
plt.ylabel("Current I (Amp)")
plt.show()
