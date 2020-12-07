import usocket
import utime

class AVR:
    CONST_INPUT_MODE_DIGITAL = 0
    CONST_INPUT_MODE_ANALOG = 1

    def __init__(self, address):
        self.address = usocket.getaddrinfo(address, 23)[0][-1]

    def get_input_select(self) -> int:
        get_input_select_response = self.send_command('SD?')

        if get_input_select_response == b'SDDIGITAL\r':
            return self.CONST_INPUT_MODE_DIGITAL

        return self.CONST_INPUT_MODE_ANALOG

    def input_select_digital(self):
        print('Setting AVR input select to Digital.')
        input_select_digital_response = self.send_command('SDDIGITAL')
        print(input_select_digital_response.decode('ascii'))

    def input_select_analog(self):
        print('Setting AVR input select to Analog.')
        input_select_analog_response = self.send_command('SDANALOG')
        print(input_select_analog_response.decode('ascii'))

    def power_standby(self):
        print('Putting AVR to standby.')
        pw_standby_response = self.send_command('PWSTANDBY')
        print(pw_standby_response.decode('ascii'))

    def power_on(self):
        print('Turning on AVR')
        pw_on_response = self.send_command('PWON')
        print(pw_on_response.decode('ascii'))
        utime.sleep_ms(1000)

    def power_state(self) -> bool:
        pwstate = self.send_command('PW?')
        return bool(pwstate == b'PWON\r')

    def set_volume_level(self, value):
        if value > 100:
            value = 100

        set_volume_response = self.send_command('MV' + str(value))
        print(set_volume_response.decode('ascii'))

    def get_volume_level(self) -> int:
        vol_level = self.send_command('MV?')
        return int(vol_level.decode('ascii'))

    def volume_mute(self):
        volume_mute_response = self.send_command('MUON')
        print(volume_mute_response.decode('ascii'))

    def volume_unmute(self):
        volume_unmute_response = self.send_command('MUOFF')
        print(volume_unmute_response.decode('ascii'))

    def get_volume_mute_state(self) -> bool:
        volume_mute_state = self.send_command('MU?')

        return bool(volume_mute_state == b'MUON\r') # NOT WORKING

    def send_command(self, command) -> bytes:
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        print(self.address)
        s.connect(self.address)

        cmd = command + '\r'
        cmd = cmd.encode('ascii')
        s.send(cmd)

        res = s.recv(135)
        s.close()

        return res
