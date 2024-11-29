import csv
import sys

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from pythondaq.diode_experiment import DiodeExperiment

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)

        mainHbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(mainHbox)

        startVbox = QtWidgets.QVBoxLayout()

        start_label = QtWidgets.QLabel("Start voltage (0-3.3 V)")
        startVbox.addWidget(start_label)
        self.start_value_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.start_value_doublespinbox.setValue(0)
        self.start_value_doublespinbox.setSingleStep(0.1)
        self.start_value_doublespinbox.setMaximum(3.3)
        self.start_value_doublespinbox.setMinimum(0.0)
        startVbox.addWidget(self.start_value_doublespinbox)
        mainHbox.addLayout(startVbox)

        stopVbox = QtWidgets.QVBoxLayout()
        stop_label = QtWidgets.QLabel("Stop voltage (0-3.3 V)")
        stopVbox.addWidget(stop_label)
        self.stop_value_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.stop_value_doublespinbox.setValue(3.3)
        self.stop_value_doublespinbox.setSingleStep(0.1)
        self.stop_value_doublespinbox.setMaximum(3.3)
        self.stop_value_doublespinbox.setMinimum(0.0)
        stopVbox.addWidget(self.stop_value_doublespinbox)
        mainHbox.addLayout(stopVbox)

        repeatVbox = QtWidgets.QVBoxLayout()
        repeat_label = QtWidgets.QLabel("Repeat measurements")
        repeatVbox.addWidget(repeat_label)
        self.repeat_value_spinbox = QtWidgets.QSpinBox()
        self.repeat_value_spinbox.setValue(3)
        self.repeat_value_spinbox.setSingleStep(1)
        self.repeat_value_spinbox.setMinimum(1)
        repeatVbox.addWidget(self.repeat_value_spinbox)
        mainHbox.addLayout(repeatVbox)

        scan_start_button = QtWidgets.QPushButton("Start scan")
        vbox.addWidget(scan_start_button)
        save_button = QtWidgets.QPushButton("Save")
        vbox.addWidget(save_button)

        save_button.clicked.connect(self.save_data)
        scan_start_button.clicked.connect(self.scan)

    @Slot()
    def scan(self):

        start = self.start_value_doublespinbox.value()
        stop = self.stop_value_doublespinbox.value()
        repeats = self.repeat_value_spinbox.value()

        V_to_ADC_step = 1023 / 3.3
        start = int(start * V_to_ADC_step)
        stop = int(stop * V_to_ADC_step)

        LED_scan = DiodeExperiment("ASRL4::INSTR")
        (
            self.voltages_LED,
            self.currents_LED,
            self.errors_voltages_LED,
            self.errors_currents_LED,
        ) = LED_scan.scan(start, stop, repeats)

        self.voltage_array = np.array(self.voltages_LED)
        self.current_array = np.array(self.currents_LED)
        self.voltage_error_array = np.array(self.errors_voltages_LED)
        self.current_error_array = np.array(self.errors_currents_LED)

        self.plot_widget.clear()
        self.plot()

    def plot(
        self,
    ):
        """Plot the function given by user, along with given resolution and domain"""
        self.plot_widget.plot(
            self.voltage_array,
            self.current_array,
            symbol="o",
            pen=None,
        )

        error_bars = pg.ErrorBarItem(
            x=self.voltage_array,
            y=self.current_array,
            width=1 * self.voltage_error_array,
            height=1 * self.current_error_array,
        )
        self.plot_widget.addItem(error_bars)
        self.plot_widget.setLabel("left", "current [A]")
        self.plot_widget.setLabel("bottom", "voltage [V]")

    @Slot()
    def save_data(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        print(filename)
        with open(f"{filename}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["I (A)", "U (V)", "SEM_I (A)", "SEM_U (V)"])
            for (
                current,
                voltage,
                error_current,
                error_voltage,
            ) in zip(
                self.current_array,
                self.voltage_array,
                self.current_error_array,
                self.voltage_error_array,
            ):
                writer.writerow([current, voltage, error_current, error_voltage])


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
