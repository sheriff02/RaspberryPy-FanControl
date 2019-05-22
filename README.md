# RaspberryPy

retroflag-picase (nespi+, superpi, megapi case)
RetroFlag Pi-Case Safe Shutdown

Turn switch "SAFE SHUTDOWN" to ON.

Example for RetroPie:

-------------------PWM Fan Control With PID----------------- Updated: 2019.05.22

Multi Switch Shutdown with advanced shutdown features for more natural behaviour:

If you press restart if emulator is currently running, then you will be kicked back to ES main menu.

If you press restart in ES main screen, ES will be restartet (no reboot!), good for quick saving metadata or internal saves.

If you press power-off then Raspberry will shutdown

All metadata is always saved

Multi Switch Shutdown by crcerror at here https://github.com/crcerror/retroflag-picase

-------------------Multi Switch Shutdown-----------------

Make sure internet connected.
Make sure keyboard connected.
Press F4 enter terminal.
In the terminal, type the one-line command below(Case sensitive):
wget -O - "https://raw.githubusercontent.com/sheriff02/RaspberryPy/master/fan_control.py" | sudo bash

