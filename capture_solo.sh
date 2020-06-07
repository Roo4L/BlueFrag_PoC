#!/bin/bash
#scripts for collecting informatin for debugging bluetooth connection between LeEco Le 2 and Laptop
#Phases in script collecting:
#	1 - information exactly after bluetooth controller start up
#	2 - information during first (successful) execution of simple_leak.py
#	3 - information after first execution
#	4 - information during second (failde) execution of simple_leak.py
#	5 - information after second execution
sleep 2
sudo lsof -u root > ~/BlueFrag_PoC/logs-06-06/4-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/logs-06-06/4-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/logs-06-06/4-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/logs-06-06/4-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/logs-06-06/4-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/logs-06-06/4-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/logs-06-06/4-syslog.txt

sudo python ~/BlueFrag_PoC/cve_2020_0022_export/simple_leak.py 80:1D:00:33:D8:82 70 70 5
sleep 1

sudo lsof -u root > ~/BlueFrag_PoC/logs-06-06/6-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/logs-06-06/6-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/logs-06-06/6-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/logs-06-06/6-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/logs-06-06/6-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/logs-06-06/6-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/logs-06-06/6-syslog.txt

echo Done