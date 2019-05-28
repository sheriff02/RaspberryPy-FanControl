# RaspberryPy

![img](https://github.com/sheriff02/RaspberryPy/blob/master/cooler_005_1_ed.png)

Example for RetroPie:

-------------------PWM Fan Control With PID----------------- Updated: 2019.05.28

Fan control script with PI(D) regulator:
Change pTemp and iTemp coefficients if you have another fan.
desiredTemp = XX  - temperature in celsius degrees, that fan system should to maintain.
fanPin = 18 - number of pin in GPIO numbering, where connected control signal to open transistor.


-------------------INSTALL SCRIPT-----------------

Make sure internet connected.
Make sure keyboard connected.
Press F4 enter terminal.
In the terminal, copy or type the one-line command below(Case sensitive):
wget -O - "https://raw.githubusercontent.com/sheriff02/RaspberryPy/master/fan_control.py" | sudo bash

