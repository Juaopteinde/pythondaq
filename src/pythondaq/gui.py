import sys

import numpy as np
import pyqtgraph as pg
from asteval import Interpreter
from numpy import cos, exp, pi, sin, tan
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

        self.scan()

    def scan(self):

        LED_scan = DiodeExperiment("ASRL4::INSTR")
        (
            self.voltages_LED,
            self.currents_LED,
            self.errors_voltages_LED,
            self.errors_currents_LED,
        ) = LED_scan.scan(
            600, 900, 3
        )  # start stop repeats
        self.plot()

    def plot(
        self,
    ):
        """Plot the function given by user, along with given resolution and domain"""
        self.plot_widget.plot(
            self.voltages_LED,
            self.currents_LED,
            symbol="o",
            pen=None,
        )

        error_bars = pg.ErrorBarItem(
            x=self.voltages_LED,
            y=self.currents_LED,
            width=2 * self.errors_voltages_LED,
            height=2 * self.errors_currents_LED,
        )
        self.plot_widget.addItem(error_bars)
        self.plot_widget.setLabel("left", "y-axis [units]")
        self.plot_widget.setLabel("bottom", "x-axis [units]")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
