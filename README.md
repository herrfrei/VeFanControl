# Raspberry Pi PWM fan control for Venus OS

> [!WARNING]
> **WIP!!!**
> Not useful right now!

Adds a PWM controlled fan using the CPU temperature to Victron Venus OS.

You need one free GPIO pin usable for PWM control (RPi3: GPIO 12,13,18,19, see below).

![RPi3](images/RaspberryPi3PWMpins.jpg)

## Installation

- VeFanControl requires that SetupHelper is installed first.

The easiest way to install VeFanControl is to do a "blind install" of SetupHelper and then add the RpiFanControl package
via the PackageManager menus. This installs the package for **GPIO12**. If you need to setup another pin,
you need to open a ssh connection to the RPi and call the setup manually on console (after download via PackageManager
or with `wget ...`).

Refer to SetupHelper here: https://github.com/kwindrem/SetupHelper

## Configuration

The package creates a configuration file on its first installation. Updates preserve the file and therefore the settings.

