#!/bin/bash
#scripts for collecting informatin for debugging bluetooth connection between LeEco Le 2 and Laptop
#Phases in script collecting:
#	1 - information exactly after bluetooth controller start up
#	2 - information during first (successful) execution of simple_leak.py
#	3 - information after first execution

#sudo btmon > ~/BlueFrag_PoC/issue_2/btmon.txt &
bluetooth_pid=$(adb shell 'pgrep droid.bluetooth')
adb logcat --pid $bluetooth_pid > ~/BlueFrag_PoC/issue_2/1-android-logcat.txt &
sudo lsof -u root > ~/BlueFrag_PoC/issue_2/1-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/issue_2/1-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/issue_2/1-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/issue_2/1-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/issue_2/1-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/issue_2/1-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/issue_2/1-syslog.txt

sudo python ~/BlueFrag_PoC/cve_2020_0022_export_ORIGINAL/fancy_leak.py 80:1D:00:33:D8:82 70 70 2
sleep 1

bluetooth_pid=$(adb shell 'pgrep droid.bluetooth')
adb logcat --pid $bluetooth_pid > ~/BlueFrag_PoC/issue_2/3-android-logcat.txt &
sudo lsof -u root > ~/BlueFrag_PoC/issue_2/1-lsof-all.txt
sudo lsof -u root > ~/BlueFrag_PoC/issue_2/3-lsof-all.txt
sudo dmesg > ~/BlueFrag_PoC/issue_2/3-dmesg.txt
hciconfig -a > ~/BlueFrag_PoC/issue_2/3-hciconfig.txt
bluetoothctl show > ~/BlueFrag_PoC/issue_2/3-bluetoothctl-show.txt
bluetoothctl devices > ~/BlueFrag_PoC/issue_2/3-bluetoothctl-devices.txt
bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/issue_2/3-bluetoothctl-info.txt
sudo cat /var/log/syslog > ~/BlueFrag_PoC/issue_2/3-syslog.txt
kill &!
echo Done.