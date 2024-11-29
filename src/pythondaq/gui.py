import csv
import sys

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from pythondaq.diode_experiment import DiodeExperiment, list_connected_resources

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        mainVbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        mainVbox.addWidget(self.plot_widget)
        mainHbox = QtWidgets.QHBoxLayout()
        mainVbox.addLayout(mainHbox)

        # Create connected devices combobox
        deviceVbox = QtWidgets.QVBoxLayout()
        deviceHbox = QtWidgets.QHBoxLayout()

        connecteddeviceVbox = QtWidgets.QVBoxLayout()
        connected_device_label = QtWidgets.QLabel("Connected port")
        connecteddeviceVbox.addWidget(connected_device_label)
        self.connected_device_combobox = QtWidgets.QComboBox()
        self.connected_device_combobox.addItems(list_connected_resources())
        connecteddeviceVbox.addWidget(self.connected_device_combobox)
        deviceHbox.addLayout(connecteddeviceVbox)

        identify_button = QtWidgets.QPushButton("Identify device")
        deviceHbox.addWidget(identify_button)
        deviceVbox.addLayout(deviceHbox)

        self.device_identification_textbox = QtWidgets.QTextEdit()
        self.device_identification_textbox.setReadOnly(True)
        deviceVbox.addWidget(self.device_identification_textbox)

        mainVbox.addLayout(deviceVbox)

        # Create & label start value doublespinbox
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

        # Create and label stop value doublespinbox
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

        # Create and label repeat value spinbox
        repeatVbox = QtWidgets.QVBoxLayout()
        repeat_label = QtWidgets.QLabel("Repeat measurements")
        repeatVbox.addWidget(repeat_label)
        self.repeat_value_spinbox = QtWidgets.QSpinBox()
        self.repeat_value_spinbox.setValue(3)
        self.repeat_value_spinbox.setSingleStep(1)
        self.repeat_value_spinbox.setMinimum(1)
        repeatVbox.addWidget(self.repeat_value_spinbox)
        mainHbox.addLayout(repeatVbox)

        # Create start scan button and save data button
        scan_start_button = QtWidgets.QPushButton("Start scan")
        save_button = QtWidgets.QPushButton("Save")
        mainVbox.addWidget(scan_start_button)
        mainVbox.addWidget(save_button)

        # Connect buttons to methods
        save_button.clicked.connect(self.save_data)
        scan_start_button.clicked.connect(self.scan)
        identify_button.clicked.connect(self.identify)

    @Slot()
    def identify(self):
        port = self.connected_device_combobox.currentText()

        device = DiodeExperiment(port)
        self.device_identification_textbox.setText(device.get_identification())

    @Slot()
    def scan(self):
        """Start a LED scan with start, stop, repeat values depending on value in appropriate (double)spinboxes."""

        start = self.start_value_doublespinbox.value()
        stop = self.stop_value_doublespinbox.value()
        repeats = self.repeat_value_spinbox.value()
        port = self.connected_device_combobox.currentText()

        V_to_ADC_step = 1023 / 3.3
        start = int(start * V_to_ADC_step)
        stop = int(stop * V_to_ADC_step)

        LED_scan = DiodeExperiment(port)
        (
            self.voltages_LED,
            self.currents_LED,
            self.errors_voltages_LED,
            self.errors_currents_LED,
        ) = LED_scan.scan(start, stop, repeats)

        # Convert to numpy arrays for errorbars
        self.voltage_array = np.array(self.voltages_LED)
        self.current_array = np.array(self.currents_LED)
        self.voltage_error_array = np.array(self.errors_voltages_LED)
        self.current_error_array = np.array(self.errors_currents_LED)

        # Clear plot so two scans dont overlap
        self.plot_widget.clear()
        self.plot()

    def plot(
        self,
    ):
        """Plot data and error of LED scan."""
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
        """Save data with selected filename and in selected directory."""
        # Open menu in which user can choose filename/directory
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")

        # Write data to csv file
        with open(f"{filename}", "w", newline="") as csvfile:
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
