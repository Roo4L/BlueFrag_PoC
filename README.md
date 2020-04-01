### 24.02.20

BlueFrag vulnerability was choosen as main theme of the progect.

Main information from : [https://seclists.org/fulldisclosure/2020/Feb/10](https://seclists.org/fulldisclosure/2020/Feb/10)

[https://stackoverflow.com/questions/37664813/android-programming-beginning](https://stackoverflow.com/questions/37664813/android-programming-beginning) - information about Android sdk adn KVM based virtual machines.

[http://media.blackhat.com/bh-dc-11/Avraham/BlackHat_DC_2011_Avraham-Popping_Android_Devices-Slides.pdf](http://media.blackhat.com/bh-dc-11/Avraham/BlackHat_DC_2011_Avraham-Popping_Android_Devices-Slides.pdf) - Presentation about basic exploits on Android

[http://shell-storm.org/blog/Shellcode-On-ARM-Architecture/](http://shell-storm.org/blog/Shellcode-On-ARM-Architecture/) - ShellCode on ARM architecture

Donwloaded book "Android System Programming for beginner". Pushed on google drive.

[https://www.electronics-notes.com/articles/connectivity/bluetooth/host-l2cap-sdp-gap.php](https://www.electronics-notes.com/articles/connectivity/bluetooth/host-l2cap-sdp-gap.php) - information about L2CAP and GAP

### 25.02.20

Installing Android Studio + setting android virual device in addition with KVM. Guide: [https://github.com/uw-it-aca/spacescout-android/wiki/1.-Setting-Up-Android-Studio-on-Ubuntu](https://github.com/uw-it-aca/spacescout-android/wiki/1.-Setting-Up-Android-Studio-on-Ubuntu)

First lauch of AVD. Bluetooth port is not supported in Android Studio. Moving to virtual box as [there](https://stackoverflow.com/questions/22604305/how-to-use-android-emulator-for-testing-bluetooth-application)

[Receiving HCI Bluetooth logs from Android.](http://www.fte.com/WebHelp/BPA600/Content/Documentation/WhitePapers/BPA600/Encryption/GettingAndroidLinkKey/RetrievingHCIlog.htm)

### 27.02.20

Analyzed the logs from forum. Seems like general trouble in previous patch was in strange behavior of memcpy() : when argument is below zero the memcpy is taking argument as extremely high(because memcpy argument is unsigned). But this isn't leading to system crash on Android 8 and 9. The following logic need to be further analyzed(assembler code). Still undefined method how to RCE using this bug.

### 29.02.20

Found PoC code for [system crash](https://github.com/leommxj/cve-2020-0022/blob/master/poc.c) using BlueFrag vulnerability. [Source from](https://translate.google.com/translate?hl=en&sl=auto&tl=en&u=https%3A%2F%2Fbestwing.me%2FAndroid-8.1-memcpy-func.html). Code requires knowledge of C BT libs. [Guide is here](https://people.csail.mit.edu/albert/bluez-intro/c404.html)

### 2.03.20

REMEMBER: you can use bettercap utility to trace BT devices and send HEX information

Made notes about unclear moments in crash PoC, which need further exploration.

### 3.03.20

Fully analyzed crash PoC file with my notes (some function may still persist unclear, but it's caused by lack of information. SetUped Android x86 emulator using VirtualBox (required Secure Boot disable), but process of bluetooth enabling is still not implemented. 

### 4.03.20

Successfully installed Android x86 and realised BT and BLE scanning. [Guide](https://www.pcsuggest.com/linux-bluetooth-setup-hcitool-bluez/) Trying to establish tight between Mi Phone and virtual device.

### 5.03.20
[Hcitool device init](https://gist.github.com/lexruee/7591755e7d8015f9f8b4) Seem like code doesn't crash BT device.

### 6.03.20

Conducted expiriment on several android devices. BLE module crashed successfully. After crash device reboot automaticly and return to usual pipe sequence.

### 15.03.20

Bad news: android system use ASLR. This may lead to crucial troubles in our progect. The solution can be found in method used in BlueBorn attack.

Analyzing possible memory range for my manipulations. [Google git code](https://android.googlesource.com/platform/system/bt/+/3cb7149d8fed2d7d77ceaa95bf845224c4db3baf/) Can't find function STREAM_TO_UINT16 (used for calculating partial_packet->len)

### 19.03.20

Chinese friends code was analysed. Understood mechanics of memcpy problem. Problem of memory range still unsolved. Decided to conduct dynamic debug using IDA. 

### 20.03.20

Successfully installed Android 8 (dotOS) [on LeEco Le 2](http://4pda.ru/forum/index.php?showtopic=799557&st=5040#entry70471648) for futher dynamic debugging using IDA. Rooted device with Magisk. [Installlaion guide](https://www.xda-developers.com/how-to-install-magisk/) Trying to connect device using adb, but strucked in error linked with ["text relocations](https://android.googlesource.com/platform/bionic/+/master/android-changes-for-ndk-developers.md).

### 21.03.20

[Changing boot.img variables](https://ctf-wiki.github.io/ctf-wiki/android/basic_reverse/dynamic/dynamic_debug/) in order to solve the problem above. [Guide](https://gist.github.com/gregor160300/068c06c0314c19855e999473708c7635). Facing some troubles with mkbootfs. Successfully changed boot.img variables. Compiled 3 testing newboot.img, but all tests were failed. Considering about problem in newboot.img archiving, despite package was assembled using cpio and gzip.

### 30.03.20

Successfully repacked boot.img of LeEco Le2 on custom android firmware. Failed trying to find problems in manual repacking using extracted bootimg.cfg, so decided to use Android Image Kitchen pack on linux. Repacked image now don't lead to system crash, but boot variables haven't change. Trying to figure out what caused this problem.

### 31.03.20

Figured problem above. 2 steps were done. First, root was reinstalled after changing boot.img. Second, Magisk settings were changed in Magisk Manager, so root became visible to every process in the system.

### 01.04.20

Successfully set connection between IDA PRO win version and rooted android device on custom OS. Face several troubles during establishing this connection. Most of steps were made using [following guide](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/debugging-android-libraries-using-ida/). 1) Adb had no rights to remount android device. Solved routing device with Magisk. Be careful: root modifes bootloader, so device should be rooted after changing boot.img. 2) Adb couldn't execute android_server on device. There were guilty several facts. The main, IDA version was to old and guide, which was followed was written 7 years ago. So, some of changes were made. 3)Android server and device bitness were different. Be careful and check bitness of debugged system.
