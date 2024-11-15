import csv
import os

import matplotlib.pyplot as plt

from pythondaq.diode_experiment import DiodeExperiment

# Define port connected to arduino
port = "ASRL4::INSTR"


class InvalidRange(Exception):
    """Exception for when starting value is higher than stopping value."""

    pass


class InvalidInput(Exception):
    """Exception for when given input is invalid."""

    pass


def save_data(currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED):
    """Save data from the measurement in a new .csv file.

    Args:
        currents_LED (list of float): Medians of measured currents (in Amps).
        voltages_LED (list of float): Medians of measured voltages (in Volts).
        errors_currents_LED (list of float): Standard errors of the currents.
        errors_voltages_LED (list of float): Standard errors of the voltages.

    Raises:
        InvalidInput: If user input is not 'y' or 'n' when prompted to save data.
    """
    # Ask if user wants to save the data in a .csv file
    while True:
        try:
            save_data = input(
                "Do you want to save the data in a .csv file? (y/n) \n Make sure you checked if filepath is set right! \n"
            )
            if save_data == "y":
                save_data = True
            elif save_data == "n":
                save_data = False
            else:
                raise InvalidInput
            break
        except InvalidInput:
            print("Give your answer as y or n. Please try again.")

    while save_data:
        # Explicitly set the directory
        directory = "C:/Users/groepA/OneDrive - UvA/Pyhton repo/Jaar 2/ECPC/pythondaq"

        # Make sure the directory exists
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist. Please check the path.")
            break

        entries = os.listdir(directory)

        # Check if the current filename already exists in the specified directory
        filename = "metingen_0.csv"
        counter = 0
        while filename in entries:
            counter += 1
            filename = f"metingen_{counter}.csv"

        filepath = os.path.join(directory, filename)

        # Create file with the new filename
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["I", "U", "SEM_I", "SEM_U"])
            for (
                current,
                voltage,
                error_current,
                error_voltage,
            ) in zip(
                currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED
            ):
                writer.writerow([current, voltage, error_current, error_voltage])

        print(f"Data saved successfully to {filepath}")
        save_data = False


# Ask user for starting value, stopping value, and amount of repeats per value.
# Raise exceptions when given values are out of bounds.
def take_inputs():
    """Ask user for start and stop value for scan, also asks for amount of repeat measurements per ADC value.

    Raises:
        InvalidRange: If the starting value is greater than or equal to the stopping value.
        InvalidInput: If the input values are outside the range of 0-1023 or repeat count is negative.
        ValueError: If a non-integer value is entered.

    Returns:
        tuple: Three integers for the starting ADC value, stopping ADC value, and the number of repeats.
    """
    while True:
        try:
            # Ask user for starting value
            start = int(
                input(
                    "Give the starting value for the scan, in ADC voltage between 0-1023 \n"
                )
            )

            if start < 0 or start > 1023:
                raise InvalidRange(
                    "The given stopping value was higher than the starting value. Please try again."
                )

            # Ask user for stopping value
            stop = int(
                input(
                    "Give the stopping value for the scan, in ADC voltage between 0-1023 \n"
                )
            )

            if stop < 0 or stop > 1023:
                raise InvalidInput(
                    "The given value is out the expected range. The range is 0 - 1023. Please try again."
                )

            if stop < start:
                raise InvalidRange(
                    "The given stopping value was higher than the starting value. Please try again."
                )

            # Ask for amount of repeat measurements per ADC value
            repeats = int(
                input("How many times do you want to repeat the measurement? \n")
            )

            if repeats < 0:
                raise InvalidInput(
                    "Repeats have to be a positive integer. Please try again."
                )
            break

        # Raise exception when given value is not integer
        except ValueError:
            print("All values should be integers. Please try again.")
        except InvalidInput as e:
            print(e)  # Print error message and loop will continue
        except InvalidRange as e:
            print(e)  # Print error message and loop will continue

    return start, stop, repeats


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


def main():
    """Runs a diode experiment, plots the data, and optionally saves it.

    Collects user inputs for the scan, performs the diode experiment, plots the data,
    and prompts the user to save the data in a .csv file.
    """

    # initialize parameters for take_inputs()
    start, stop, repeats = take_inputs()

    # Run measurements and save the data
    measurement = DiodeExperiment(port)
    voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = (
        measurement.scan(int(start), int(stop), repeats)  # start stop repeats
    )

    plot_data(voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED)

    save_data(currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED)


if __name__ == "__main__":
    main()
