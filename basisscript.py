import pyvisa

rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL4::INSTR", read_termination="\r\n", write_termination="\n"
)
identification = device.query("*IDN?")

# Convert raw 10 bit value to volt
def raw_value_to_volt(raw_value):
    step = 3.3/1023
    volt = raw_value * step
    return volt

# Convert volt to 10 bit value
def volt_to_raw_value(volt):
    step = 1023/3.3
    raw_value = step * volt
    return raw_value



for voltage in range(0,1024):
    device.query(f"OUT:CH0 {voltage}")
    raw_value_LED = device.query("OUT:CHxx?")
    raw_value_resistor = device.query("OUT:CHxx?")
    voltage_LED = raw_value_to_volt(raw_value_LED)
    voltage_resistor = raw_value_to_volt(raw_value_resistor)
    print(f"Raw value voltage over LED is {raw_value_LED}. Voltage is {voltage_LED}.")
    print(f"Raw value voltage over resistor is {raw_value_resistor}. Voltage is {voltage_resistor}.")
    biem