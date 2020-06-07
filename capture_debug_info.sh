#!/bin/bash
#scripts for collecting informatin for debugging bluetooth connection between LeEco Le 2 and Laptop
#Phases in script collecting:
#	1 - information exactly after bluetooth controller start up
#	2 - information during first (successful) execution of simple_leak.py
#	3 - information after first execution
#	4 - information during second (failde) execution of simple_leak.py
#	5 - information after second execution
rfkill block bluetooth
rfkill unblock bluetooth
sleep 2
#sudo btmon > ~/BlueFrag_PoC/logs-06-06/btmon.txt &
sudo lsof -u root > ~/BlueFrag_PoC/logs-06-06/1-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/logs-06-06/1-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/logs-06-06/1-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/logs-06-06/1-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/logs-06-06/1-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/logs-06-06/1-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/logs-06-06/1-syslog.txt

sudo python ~/BlueFrag_PoC/cve_2020_0022_export/simple_leak.py 80:1D:00:33:D8:82 70 70 2
sleep 1

sudo lsof -u root > ~/BlueFrag_PoC/logs-06-06/3-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/logs-06-06/3-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/logs-06-06/3-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/logs-06-06/3-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/logs-06-06/3-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/logs-06-06/3-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/logs-06-06/3-syslog.txt

sudo python ~/BlueFrag_PoC/cve_2020_0022_export/simple_leak.py 80:1D:00:33:D8:82 70 70 4

sudo lsof -u root > ~/BlueFrag_PoC/logs-06-06/5-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/logs-06-06/5-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/logs-06-06/5-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/logs-06-06/5-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/logs-06-06/5-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/logs-06-06/5-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/logs-06-06/5-syslog.txt

#kill &!
echo Done.