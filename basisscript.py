import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
device = rm.open_resource(
    "ASRL4::INSTR", read_termination="\r\n", write_termination="\n"
)
identification = device.query("*IDN?")


# Convert raw 10 bit value to volt
def raw_value_to_volt(raw_value):
    step = 3.3 / 1023
    volt = raw_value * step
    return volt


# Convert volt to 10 bit value
def volt_to_raw_value(volt):
    step = 1023 / 3.3
    raw_value = step * volt
    return raw_value


# Up the current from min to max, measure and calculate voltages & current
for voltage in range(0, 1024):

    # Change outgoing voltage
    device.query(f"OUT:CH0 {voltage}")

    # Measure voltages over resistor & LED
    raw_value_resistor = int(device.query("MEAS:CH2?"))
    raw_value_LED = int(device.query("MEAS:CH1?")) - int(device.query("MEAS:CH2?"))

    # Convert raw values to volt
    voltage_LED = raw_value_to_volt(raw_value_LED)
    voltage_resistor = raw_value_to_volt(raw_value_resistor)

    # Calculate current for 220 Ohm resistor
    current = voltage_resistor / 220

    print(
        f"Outgoing voltage = {raw_value_to_volt(int(device.query("OUT:CH0?")))}, raw value = {device.query("OUT:CH0?")}"
    )
    print(f"Raw value voltage over LED is {raw_value_LED}. Voltage is {voltage_LED}.")
    print(
        f"Raw value voltage over resistor is {raw_value_resistor}. Voltage is {voltage_resistor}."
    )
