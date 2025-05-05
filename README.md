# HM71-Remote-CMD

Remake of App Android "Pioneer Remote App" in Python 3 for Desktop.

Python script that allows you to remotely control a Pioneer device with Wi-Fi controllable via telnet.

To create it I used my X-HM71-K, so I guarantee the compatibility whith this family of products.

I could not test the service that acquires audio files from an Ipod, since I do not have this device.

Installation
------------
The script works with python3.

So it is necessary to have an installation on board.

For Linux it is preinstalled in all distributions.
For Windows it can be downloaded at the link https://www.python.org/downloads/windows/
For macOS it is not recommended to use the native installed one (Python2) but to download it from https://www.python.org/downloads/macos/

If it is not already available it is necessary to install Tkinter
Useful information is available on this site https://codeloop.org/how-to-install-tkinter-in-windows-linux/
On macOS and Windows, using the versions that I recommended, you should find it preset.

On macOS be careful to launch it with "python3 HM71-Remote-CMD.py"

If you have a version of Python 3.13 or higher and this error occurs:

localhost@user:HM71-Remote-CMD$ ./HM71-Remote-CMD.py
Traceback (most recent call last):
File "./HM71-Remote-CMD.py", line 7, in <module>
import telnetlib
ModuleNotFoundError: No module named 'telnetlib'

install this library https://pypi.org/project/telnetlib-313-and-up/

Configuration
--------------
Before running the program for the first time, edit HM71-Remote-CMD.ini which must be in the same directory as HM71-Remote-CMD.py.

HM71_HOST = 192.168.x.x (Enter the ip of the pioneer device)
HM71_PORT = 8102 (Verify that it is the correct port)

Debug is switchable on/off:
;HM71_DEBUG = True
HM71_DEBUG = False

Set HM71_Ini_editor with your favorite editor:
;HM71_Ini_editor kwrite@KDE gedit@Gnome notepad@Windows open@macOS
HM71_Ini_editor = "/usr/bin/kwrite"
; HM71_Ini_editor = "/usr/bin/gedit"
; HM71_Ini_editor = "notepad"
; HM71_Ini_editor = "open"

You can put a description for the preset stations in the Turner:
HM71_Turner_PRES_01 = "Radio 01"
HM71_Turner_PRES_02 = "Radio 02"
HM71_Turner_PRES_03 = "Radio 03"
HM71_Turner_PRES_04 = "Radio 04"

Execution
----------
python3 HM71-Remote-CMD.py
