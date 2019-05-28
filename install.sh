#!/bin/bash


#Step 1) Check if root--------------------------------------
if [[ $EUID -ne 0 ]]; then
   echo "Please execute script as root." 
   exit 1
fi
#-----------------------------------------------------------

#Step 2) enable UART----------------------------------------
cd /boot/
File=config.txt
if grep -q "enable_uart=1" "$File";
	then
		echo "UART already enabled. Doing nothing."
	else
		echo "enable_uart=1" >> $File
		echo "UART enabled."
fi
#-----------------------------------------------------------

#Step 3) Update repository----------------------------------
sudo apt-get update -y
#-----------------------------------------------------------

#Step 4) Install gpiozero module----------------------------
sudo apt-get install -y python3-gpiozero
#-----------------------------------------------------------

#Step 5) Download Python script-----------------------------
cd /opt/
sudo mkdir FanControl
cd /opt/FanControl
script=fan_control.py

if [ -e $script ];
	then
		echo "Script fan_control.py already exists. Doing nothing."
	else
		wget "https://raw.githubusercontent.com/sheriff02/RaspberryPy/master/fan_control.py"
fi
#-----------------------------------------------------------

#Step 6) Enable Python script to run on start up------------
cd /etc/
RC=rc.local

if grep -q "sudo python3 \/opt\/FanControl\/fan_control.py \&" "$RC";
	then
		echo "File /etc/rc.local already configured. Doing nothing."
	else
		sed -i -e "s/^exit 0/sudo python3 \/opt\/FanControl\/fan_control.py \&\n&/g" "$RC"
		echo "File /etc/rc.local configured."
fi
#-----------------------------------------------------------

#Step 7) Reboot to apply changes----------------------------
echo "FanControl installation done. Will now reboot after 3 seconds."
sleep 3
sudo reboot
#-----------------------------------------------------------









