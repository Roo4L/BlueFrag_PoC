import os
import sys

in_file = str(sys.argv[1])
out_file = "-parsed.".join(in_file.split("."))

a = [0 for i in range(10000)]
buf = [0 for i in range(10)]
f = open(in_file, "r")
length = 0;
for line in f:
	buf = line.split();
	a[length] = " ".join(buf[4:])
	length += 1;
f.close()

f = open(out_file, "w")
for i in range(length):
	f.write(a[i] + "\n");
f.close()
