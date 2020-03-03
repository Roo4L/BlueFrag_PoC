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

