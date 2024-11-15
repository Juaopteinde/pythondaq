import click

from pythondaq.diode_experiment import DiodeExperiment


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
def view_scan(port, starting_voltage, stopping_voltage, repeats):

    V_to_ADC_step = 1023 / 3.3
    starting_value = int(starting_voltage * V_to_ADC_step)
    stopping_value = int(stopping_voltage * V_to_ADC_step)

    LED_scan = DiodeExperiment(port)
    voltages_LED, currents_LED, errors_voltages_LED, errors_currents_LED = (
        LED_scan.scan(starting_value, stopping_value, repeats)
    )
    print(voltages_LED, currents_LED)


if __name__ == "__main__":
    view_group()
