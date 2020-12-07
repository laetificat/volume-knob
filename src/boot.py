# boot.py - - runs on boot-up
import network

def do_connect():
    print('Disabling Access Point...')
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    print('Access Point disabled.')

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('', '')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    print('======================================\n')

do_connect()
