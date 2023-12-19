#! /usr/bin/env python3
#
# writes GPIO pin given as PWM pin to config file, exits with 1 on failure

from fan_control import read_config, get_pwm_channel, write_config
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need the pwm pin to use as argument!")
        sys.exit(1)
    try:
        cfg = read_config()
        pwm_pin = int(sys.argv[1])        
        pwm_chan = get_pwm_channel(pwm_pin)
        if pwm_chan < 0:
            print(f"Invalid pwm pin {pwm_pin} given!")
            sys.exit(1)
        cfg['pwm_pin'] = pwm_pin
        res = write_config(cfg)
        sys.exit(0 if res else 1)
    except Exception as e:
        print(f"Error occured: {e}")
        sys.exit(1)
