import csv
import os

import click
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Model

from pythondaq.diode_experiment import DiodeExperiment, list_connected_resources


class SearchError(Exception):
    """Exception for when search str does not yield a single device."""

    pass


def plot_data(voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED):
    """Plots data from scan in diode_experiment.

    Args:
        voltages_LED (list of float): List of measured voltages (in Volts).
        currents_LED (list of float): List of measured currents (in Amps).
        errors_voltages_LED (list of float): List of voltage measurement errors.
        errors_currents_LED (list of float): List of current measurement errors.
    """

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


def save_data(
    currents_LED,
    voltages_LED,
    errors_currents_LED,
    errors_voltages_LED,
    filename,
    output_directory,
):
    """Save scan data into a new .csv file in a set or current directory.
    \n

    Savedata directory priority:
        (1) output_directory
        (2) current directory


    Args:
        currents_LED (list of float): medians of measured currents (in Amps)
        voltages_LED (list of float): medians of measured voltages (in Volts)
        errors_currents_LED (list of float): standard errors of the currents
        errors_voltages_LED (list of float): standard errors of the voltages
        filename (str): name for the .csv file containing scan data
        output_directory (str): directory to save .csv file in

    """

    # Save data only if filename is given
    if output_directory:
        # Set directory to given directory, or to current if no directory is given
        directory = os.path.normpath(output_directory)
        if not os.path.isdir(directory):
            raise ValueError(
                f"The specified output directory does not exist: {directory}"
            )
    else:
        directory = os.getcwd()

    # Check if the current filename already exists in the specified directory
    # If so, iterate the filename to filename(1), filename(2), etc.
    entries = os.listdir(directory)

    original_filename = filename
    if f"{original_filename}.csv" in entries:
        counter = 0
        while f"{filename}.csv" in entries:
            counter += 1
            filename = f"{original_filename}({counter})"

    # Write scan data into .csv file located at filepath
    filepath = os.path.join(directory, filename)

    with open(f"{filepath}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["I (A)", "U (V)", "SEM_I (A)", "SEM_U (V)"])
        for (
            current,
            voltage,
            error_current,
            error_voltage,
        ) in zip(currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED):
            writer.writerow([current, voltage, error_current, error_voltage])

    print(f"Data saved successfully to {filepath}")


# Create group of commands for diode
@click.group()
def diode():
    """Parent command of info, list, scan."""
    pass


@diode.command("info")
@click.argument("search")
def info(search):
    """Retreive and print identification string of connected device.

    Args:
        search (str): string to look for in list of connected devices

    Raises:
        SearchError: if search string does not yield a single device
    """

    connected_ports = list_connected_resources()
    devices_list = []
    for device in connected_ports:
        if search in device:
            devices_list.append(device)

    if len(devices_list) > 1 or len(devices_list) == 0:
        raise SearchError(
            f"Search str must only return 1 device in diode list, not {len(devices_list)}"
        )

    print(devices_list)
    arduino_device = DiodeExperiment(devices_list[0])
    identification = arduino_device.get_identification()

    print(identification)


@diode.command("list")
@click.option("-s", "--search", required=False)
def view_list(search):
    """Retreive and print list of connected devices.

    Args:
        search (str): string to look for in list of connected devices
    """
    connected_ports = list_connected_resources()
    if search:
        search_devices = []
        for device in connected_ports:
            if search in device:
                search_devices.append(device)
        print("The devices that match your search string:\n")
        for device in search_devices:
            print(device)
    else:
        print("The device connected to your computer:\n")
        for port in connected_ports:
            print(port)


# Command to start LED scan
@diode.command("scan")
@click.argument(
    "port",
)
@click.option(
    "-s",
    "-start",
    "--starting_voltage",
    default=0.0,
    help="Starting voltage for the scan.",
)
@click.option(
    "-e",
    "-end",
    "-stop",
    "--stopping_voltage",
    default=3.3,
    help="Stopping voltage for the scan.",
)
@click.option(
    "-r",
    "--repeats",
    default=3,
    help="Amount of measurements to run per ADC voltage value of the scan.",
)
@click.option(
    "-o",
    "--output",
    type=str,
    required=False,
    help="Store data into .csv file with given filename. Will not store data if not given.",
)
@click.option(
    "-od",
    "--output-directory",
    type=str,
    required=False,
    help="Give directory you want to save data in. If not given, will store data into directory set in code or current directory if -cd is given.",
)
@click.option(
    "-g",
    "--graph",
    is_flag=True,
    default=False,
    help="Toggle graphing the data.",
)
@click.option(
    "--shockley",
    is_flag=True,
    default=False,
    help="Toggle fitting the data to shockley formula.",
)
def view_scan(
    port,
    starting_voltage,
    stopping_voltage,
    repeats,
    output,
    output_directory,
    graph,
    shockley,
):
    """Start a LED scan in a given voltage range. Plot and optionally save the data.
    \n
    \b
    Savedata directory priority:
        (1) If output_directory correctly provided, savedata goes there.
        (2) If output_directoy not provided, savedata goes to current directory.
    \b
    Args:
        port (str): port connected to Arduino

    Raises:
        SearchError: if provided search string does not yield a single connected device.

    """

    V_to_ADC_step = 1023 / 3.3
    starting_value = int(starting_voltage * V_to_ADC_step)
    stopping_value = int(stopping_voltage * V_to_ADC_step)

    # Check whether search string only applies to single device
    # reason is code won't work with >1 devices
    connected_ports = list_connected_resources()
    devices_list = []
    for device in connected_ports:
        if port in device:
            devices_list.append(device)
    if len(devices_list) > 1 or len(devices_list) == 0:
        raise SearchError(
            f"Search str must only return 1 device in diode list, not {len(devices_list)}"
        )

    LED_scan = DiodeExperiment(port)
    voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = (
        LED_scan.scan(starting_value, stopping_value, repeats)
    )

    print(voltages_LED, currents_LED)

    if graph:
        plot_data(voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED)

    if output:
        save_data(
            currents_LED,
            voltages_LED,
            errors_currents_LED,
            errors_voltages_LED,
            output,
            output_directory,
        )

    if shockley:

        # Shockley formula: I = Is * (exp(Vd/n*Vt) - 1)
        # 'n' parameter has been left out
        # reason is fit having trouble with 3rd parameter
        def shockley(V_d, I_s, V_t):
            return I_s * (np.exp((V_d) / (V_t)) - 1)

        smodel = Model(shockley)
        params = smodel.make_params(I_s=0, V_t=0.01)
        result = smodel.fit(currents_LED, params, V_d=voltages_LED)

        print(result.fit_report())
        V_t_fitted = result.params["V_t"].value
        fitted_currents = result.best_fit

        k = (V_t_fitted * 1.602e-19) / 300
        print(f"Boltzmann constant = {k}")

        plt.plot(voltages_LED, currents_LED, ".", label="Scan")
        plt.plot(voltages_LED, fitted_currents, ".", label="Fit")
        plt.legend(loc="best")
        plt.title("Shockley fit of LED scan")
        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.show()


if __name__ == "__main__":
    diode()
