import csv
import os

import matplotlib.pyplot as plt

from diode_experiment import DiodeExperiment

# Define port connected to arduino
port = "ASRL4::INSTR"


# Exception for when given ADC value is out of range
class OutOfRange:
    pass


# Exception for when starting value is higher than stopping value
class InvalidRange:
    pass


class WrongInput:
    pass


# Ask user for starting value, stopping value, and amount of repeats per value.\
# Raise exceptions when given values are out of bounds.\
while True:
    try:
        # Ask user for starting value
        start = int(
            input(
                "Give the starting value for the scan, in ADC voltage between 0-1023 \n"
            )
        )

        if start < 0 or start > 1023:
            raise OutOfRange

        # Ask user for stopping value
        stop = int(
            input(
                "Give the stopping value for the scan, in ADC voltage between 0-1023 \n"
            )
        )

        if stop < 0 or stop > 1023:
            raise OutOfRange

        if stop < start:
            raise InvalidRange

        # Ask for amount of repeat measurements per ADC value
        repeats = int(input("How many times do you want to repeat the measurement? \n"))
        break

    # Raise exception when given value is not integer
    except ValueError:
        print("All values should be integers. Please try again.")

    # Raise exception when value is out of range
    except OutOfRange:
        print(
            "The given value is out the expected range. The range is 0 - 1023. Please try again."
        )

    # Raise exception when start > stop
    except InvalidRange:
        print(
            "The given stopping value was higher than the starting value. Please try again."
        )

# Ask if user wants to save the data in a .csv file
while True:
    try:
        save_data = input("Do you want to save the data in a .csv file? (y/n) \n")
        if save_data == "y":
            save_data = True
        elif save_data == "n":
            save_data = False
        else:
            raise SyntaxError
        break
    except SyntaxError:
        print("Give your answer as y or n. Please try again.")


# Run measurements and save the data
measurement = DiodeExperiment(port)
voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = measurement.scan(
    int(start), int(stop), 3  # start stop repeats
)

# Save the data in a .csv file if save_data == True
# Does currently not work sadly
while save_data:

    # Create a list of all files in the current directory
    current_directory = os.getcwd()
    entries = os.listdir(current_directory)

    # Check if the current filename already exists in the current directory, if not create a new filename
    filename = "metingen_0.csv"
    counter = 0
    while filename in entries:
        filename = f"metingen_{counter}.csv"
        counter += 1

    # Create file with the new filename
    with open(f"{filename}", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["I", "U", "SEM_I", "SEM_U"])
        for currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED in zip(
            currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED
        ):
            writer.writerow(
                [currents_LED, voltages_LED, errors_currents_LED, errors_voltages_LED]
            )

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
