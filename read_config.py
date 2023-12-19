#! /usr/bin/env python3
from fan_control import read_config


if __name__ == "__main__":
    cfg = read_config()
    for key,value in cfg.items():
        if isinstance(value, str):
            print(f'{key}="{value}"')
        else:
            print(f'{key}={value}')
