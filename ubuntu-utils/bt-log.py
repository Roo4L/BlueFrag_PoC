import os 
import subprocess

exit_code = subprocess.run(["adb","shell"], stdout = subprocess.PIPE, input = "pgrep bluetooth\nexit\n")

x = sys.stdout.readline()
y = sys.stdout.readline()

sys.stdin.writeline("exit\n")
os.system("adb logcat --pid %d", y.split()[1])
os.wait()