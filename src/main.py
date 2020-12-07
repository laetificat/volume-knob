import machine
import utime
import denon

avr = denon.AVR("")

pin12 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

pwr_pressed = None
pwr_command_executed = False

while True:
    # Knob is pressed
    if pin12.value() == 0:
        if pwr_pressed is None:
            pwr_pressed = utime.ticks_ms()

        if utime.ticks_diff(utime.ticks_ms(), pwr_pressed) > 2000 and not pwr_command_executed:
            if not avr.power_state():
                avr.power_on()
            else:
                avr.power_standby()

            pwr_command_executed = True

    # Knob is not pressed (anymore)
    if pin12.value() == 1 and pwr_pressed is not None:
        pwr_pressed = None

        if utime.ticks_diff(utime.ticks_ms(), pwr_pressed) > 2000 and pwr_command_executed:
            pwr_command_executed = False
            continue

        if not avr.power_state():
            avr.power_on()
            continue

        if avr.get_input_select() == avr.CONST_INPUT_MODE_DIGITAL:
            avr.input_select_analog()
        else:
            avr.input_select_digital()
