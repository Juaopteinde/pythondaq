import csv
import os

import click
import matplotlib.pyplot as plt

from pythondaq.diode_experiment import DiodeExperiment


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
    current_directory,
):
    """Save data from the measurement in a new .csv file.

    Args:
        currents_LED (list of float): Medians of measured currents (in Amps).
        voltages_LED (list of float): Medians of measured voltages (in Volts).
        errors_currents_LED (list of float): Standard errors of the currents.
        errors_voltages_LED (list of float): Standard errors of the voltages.

    Raises:
        InvalidInput: If user input is not 'y' or 'n' when prompted to save data.
    """

    # Explicitly set the directory
    if current_directory:
        directory = os.getcwd()
    else:
        directory = (
            "C:/Users/groepA/OneDrive - UvA/Pyhton repo/Jaar 2/ECPC/pythondaq/metingen"
        )

    entries = os.listdir(directory)
    print(entries)

    # Check if the current filename already exists in the specified directory
    original_filename = filename
    if f"{original_filename}.csv" in entries:
        counter = 0
        while f"{filename}.csv" in entries:
            counter += 1
            filename = f"{original_filename}({counter})"

    filepath = os.path.join(directory, filename)

    # Create file with the new filename
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


@click.group()
def view_group():
    pass


@view_group.command("list")
def view_list():
    print("Work in progress, list devices")


@view_group.command("scan")
@click.option("-p", "--port", default="ASRL4::INSTR")
@click.option("-s", "-start", "--starting_voltage", default=0.0)
@click.option("-e", "-end", "-stop", "--stopping_voltage", default=3.3)
@click.option("-r", "--repeats", default=3)
@click.option("-f", "-o", "--output", type=str, required=False)
@click.option("-cd", "--current_directory", is_flag=True, default=False)
def view_scan(
    port, starting_voltage, stopping_voltage, repeats, output, current_directory
):

    V_to_ADC_step = 1023 / 3.3
    starting_value = int(starting_voltage * V_to_ADC_step)
    stopping_value = int(stopping_voltage * V_to_ADC_step)

    LED_scan = DiodeExperiment(port)
    voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = (
        LED_scan.scan(starting_value, stopping_value, repeats)
    )
    # plot_data(voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED)
    if output:
        save_data(
            currents_LED,
            voltages_LED,
            errors_currents_LED,
            errors_voltages_LED,
            output,
            current_directory,
        )


if __name__ == "__main__":
    view_group()
    view_group()
    view_group()
    view_group()
