from diode_experiment import DiodeExperiment
import matplotlib.pyplot as plt


port = xxx
measurement = DiodeExperiment(port)
voltages_LED, currents_LED = measurement.scan(0, 1024)

plt.plot(voltages_LED, currents_LED)
plt.show()
