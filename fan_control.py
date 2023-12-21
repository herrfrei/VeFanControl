#!/usr/bin/env python3
#
# PWM fan control program

import os.path
import json
import time
import signal
import sys

from rpi_hw import get_cpu_temperature
from pwm import PWM

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'fan_control.cfg')

# PWM_FREQ = 25  # [Hz] PWM frequency
#
# FAN_CHANNEL = 0  # BCM pwm channel used to drive fan
# WAIT_TIME = 10  # [s] Time to wait between each refresh
#
# OFF_TEMP = 40  # [°C] temperature below which to stop the fan
# MIN_TEMP = 45  # [°C] temperature above which to start the fan
# MAX_TEMP = 70  # [°C] temperature at which to operate at max fan speed
# FAN_LOW = 1
# FAN_HIGH = 100
# FAN_OFF = 0
# FAN_MAX = 100
# FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)


options = {    
    'pwm_pin': 12,       # BCM PWM pin
    'pwm_freq':  25,     # [Hz] PWM frequency
    'wait_time': 10,     # [s] Time to wait between each refresh
    'off_temp':  40,     # [°C] temperature below which to stop the fan
    'min_temp':  45,     # [°C] temperature above which to start the fan
    'max_temp':  70,     # [°C] temperature at which to operate at max fan speed
    'off_pwm':   0.0,    # PWM value for OFF state
    'min_pwm':   1.0,    # Minimum PWM value
    'max_pwm':   100.0,  # Minimum PWM value
}

# fan_control_settings = {
#     'pwm_freq':  ['/Settings/FanControl/PwmFreq', 25, 10, 1000],        # [Hz] PWM frequency
#     'pwm_chan':  ['/Settings/FanControl/PwmChan', 0, 0, 1],             # BCM pwm channel used to drive fan
#     'wait_time': ['/Settings/FanControl/WaitTime', 10, 1, 60],          # [s] Time to wait between each refresh
#     'off_temp':  ['/Settings/FanControl/OffTemp', 40, 10, 50],          # [°C] temperature below which to stop the fan
#     'min_temp':  ['/Settings/FanControl/MinTemp', 45, 20, 50],          # [°C] temperature above which to start the fan
#     'max_temp':  ['/Settings/FanControl/MaxTemp', 70, 30, 80],          # [°C] temperature at which to operate at max fan speed
#     'off_pwm':   ['/Settings/FanControl/OffPwm', 0.0, 0.0, 1.0],        # PWM value for OFF state
#     'min_pwm':   ['/Settings/FanControl/MinPwm', 1.0, 1.0, 20.0],       # Minimum PWM value
#     'max_pwm':   ['/Settings/FanControl/MaxPwm', 100.0, 80.0, 100.0],   # Minimum PWM value
# }


# PWM0: 12,4(Alt0) 18,2(Alt5) 40,4(Alt0)            52,5(Alt1)
# PWM1: 13,4(Alt0) 19,2(Alt5) 41,4(Alt0) 45,4(Alt0) 53,5(Alt1)

def get_pwm_channel(pwm_pin: int) -> int:
    pwm_pin2chan = { 12: 0, 13: 1, 18: 0, 19: 1 }
    if pwm_pin in pwm_pin2chan:
        return pwm_pin2chan[pwm_pin]
    return -1
    

def get_pin_func(pwm_pin: int) -> int:
    pwm_pin2func = { 12: 4, 13: 4, 18: 2, 19: 2 }
    if pwm_pin in pwm_pin2func:
        return pwm_pin2func[pwm_pin]
    return -1

    
def read_config(defaults: dict = options) -> dict:
    cfg = defaults
    try:
        if not os.path.exists(CONFIG_FILE):
            # write default settings to file
            with open(CONFIG_FILE, 'w') as f:
                json.dump(defaults, f)
        with open(CONFIG_FILE, 'r') as f:
            cfg = json.load(f)
        cfg['pwm_chan'] = get_pwm_channel(cfg['pwm_pin'])
        if cfg['pwm_chan'] < 0:
            print(f"Invalid PWM pin {cfg['pwm_pin']} given!")
            sys.exit(1)
        cfg['pin_func'] = get_pin_func(cfg['pwm_pin'])
        if cfg['pin_func'] < 0:
            print(f"Invalid PWM pin {cfg['pwm_pin']} given!")
            sys.exit(1)
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        return cfg


def write_config(cfg: dict) -> bool:
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(cfg, f)
        return True
    except Exception as e:
        print(f"Error occured: {e}")
        return False


def handle_fan_speed(fan, cfg, fan_gain, temperature):
    # print(temperature)
    if temperature > cfg['min_temp']:
        delta = min(temperature, cfg['max_temp']) - cfg['min_temp']
        fan.set_duty_cycle(cfg['min_pwm'] + delta * fan_gain)

    elif temperature < cfg['off_temp']:
        fan.set_duty_cycle(cfg['off_pwm'])


def main():
    fan = None
    cfg = read_config(options)
    fan_gain = float(cfg['max_pwm'] - cfg['min_pwm']) / float(cfg['max_temp'] - cfg['min_temp'])
    try:
        signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
        if get_pwm_channel(cfg['pwm_pin']) < 0:
            print(f"Invalid PWM pin {cfg['pwm_pin']} given!")
            sys.exit(1)
        fan = PWM(cfg['pwm_chan'])
        fan.initialize()
        fan.set_period(cfg['pwm_freq'])
        fan.enable()
        while True:
            handle_fan_speed(fan, cfg, fan_gain, get_cpu_temperature())
            time.sleep(cfg['wait_time'])
    except KeyboardInterrupt:
        pass
    finally:
        if fan is not None:
            fan.deinitialize()


if __name__ == "__main__":
    main()
