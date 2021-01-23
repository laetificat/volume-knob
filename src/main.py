import machine
import utime
import denon
import rotary

avr = denon.AVR("")

pin14 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
pin12 = machine.Pin(12, machine.Pin.IN)
pin13 = machine.Pin(13, machine.Pin.IN)

pwr_pressed = None
pwr_command_executed = False

r = rotary.RotaryIRQ(pin_num_clk=12, 
                    pin_num_dt=13, 
                    min_val=0, 
                    max_val=100, 
                    reverse=False, 
                    range_mode=rotary.RotaryIRQ.RANGE_BOUNDED)

r.set(value=avr.get_volume_level())
vol_old = r.value()

while True:
    vol_new = r.value()
    
    if vol_old != vol_new:
        vol_old = vol_new
        avr.set_volume_level(vol_old)

    # Knob is pressed
    if pin14.value() == 0:
        if pwr_pressed is None:
            pwr_pressed = utime.ticks_ms()

        if utime.ticks_diff(utime.ticks_ms(), pwr_pressed) > 2000 and not pwr_command_executed:
            if not avr.power_state():
                avr.power_on()
            else:
                avr.power_standby()

            pwr_command_executed = True

    # Knob is not pressed (anymore)
    if pin14.value() == 1 and pwr_pressed is not None:
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
