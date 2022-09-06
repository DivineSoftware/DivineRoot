from adbutils import adb
#import androguard
import os
import random
from colorama import Fore
import colorama
colorama.init()
import rainbowtext

logo = rainbowtext.text("""
/*******                             /**  
/**////**                            |**  
/**    /** ******  ******   ******  ******
/**    /**//**//* **////** **////**///**/ 
/**    /** /** / /**   /**/**   /**  /**  
/**    **  /**   /**   /**/**   /**  /**  
/*******  /***   //****** //******   //** 
///////   ///     //////   //////     //  
No warranty ;)\n""")
tips = [Fore.LIGHTBLUE_EX + 'Pro tip: Use recovery command to flash any recovery to bootloader, it allows you to install own operating systems and root your phone easily.',
        Fore.LIGHTBLUE_EX + 'Pro tip: Do not unplug your device during rooting process otherwise you can cause system error.',
        Fore.LIGHTBLUE_EX + 'Pro tip: Backup your phone before unlocking bootloader, it will wipe your data.']
print(f"""
{logo}
{Fore.BLUE}Welcome {os.getlogin()}!
{Fore.BLUE}How-to:{Fore.CYAN}
    0. Download usb drivers for your device
    1. Enable 'usb debugging' and 'oem unlocking' in developer options ({Fore.WHITE}click 7 times build number{Fore.CYAN})
    2. Plug your phone to pc with USB connector
    3. ({Fore.RED}Unlock bootloader{Fore.CYAN}) and pick a root method or execute commands via adb shell
{Fore.BLUE}Commands:{Fore.CYAN}
   {Fore.MAGENTA}├connect{Fore.CYAN} - connect your android phone to this pc ({Fore.WHITE}serves for testing purposes{Fore.CYAN})
   {Fore.MAGENTA}├shell{Fore.CYAN} - adb ({Fore.WHITE}android debugging bridge{Fore.CYAN}) shell
   {Fore.MAGENTA}├recovery{Fore.CYAN} - flash recovery ({Fore.RED}Your recovery.img must be in the same folder{Fore.CYAN})
   {Fore.MAGENTA}├unlock (code){Fore.CYAN} - unlock bootloader ({Fore.RED}Warning, this will wipe your device!{Fore.CYAN})
   {Fore.MAGENTA}├remove (password/pattern){Fore.CYAN} - remove screen lock ({Fore.RED}Warning, this will remove screenlock feature until next update!{Fore.CYAN})
   {Fore.MAGENTA}├backup{Fore.CYAN} - backups all your data in 'backup' folder
   {Fore.MAGENTA}├restore{Fore.CYAN} - restores data from 'backup' folder
   {Fore.MAGENTA}├Root methods:
   {Fore.MAGENTA}|   ├method 1 - rooting booted device
   {Fore.MAGENTA}|   └method 2 - rooting device from bootloader (recommended)
   {Fore.MAGENTA}├readme
   {Fore.MAGENTA}├help
   {Fore.MAGENTA}└exit
{Fore.WHITE}Built with {Fore.LIGHTGREEN_EX}\U0001F40D{Fore.WHITE} and https://github.com/openatx/adbutils
{random.choice(tips)}
""")

while True:
    print(rainbowtext.text(f"""{os.getlogin()}# """), end = ''); cmd = input()
    if cmd == "connect":
        try:
            device = adb.device()
            os.system('cls || clear')
            for d in adb.device_list():
                print(rainbowtext.text(f"""
Connected!
    
Serial key: {device.serial}
Operating system: {device.prop.name}
Device: {device.prop.device}
Model: {device.prop.model}
                """))
        except:
            print("No device(s) connected!")
    elif cmd == "recovery":
        try:
            print(Fore.MAGENTA + "Note: if you have not unlocked your bootloader, this will not work")
            device = adb.device()
            print(Fore.BLUE + device.shell('reboot bootloader'))
            print(Fore.BLUE + device.shell('fastboot flash recovery.img'))
            print(Fore.BLUE + "Done!")
        except:
            print('An error has occured')
    elif cmd == "remove":
        try:
            lock = cmd.split(" ")[1]
            device = adb.device()
            if lock == "password":
                print(Fore.BLUE + device.shell('rm /data/system/gatekeeper.password.key'))
                print(Fore.BLUE + device.shell('rm /data/system/device_policies.xml'))
                print(Fore.BLUE + device.shell('rm /data/system/locksettings.db'))
                print(Fore.BLUE + "Done!")
                print("If you see 'acess denied' message, try rebooting into bootloader")
            if lock == "pattern":
                print(Fore.BLUE + device.shell('rm /data/system/gatekeeper.pattern.key'))
                print(Fore.BLUE + device.shell('rm /data/system/device_policies.xml'))
                print(Fore.BLUE + device.shell('rm /data/system/locksettings.db'))
                print(Fore.BLUE + "Done!")
                print(Fore.MAGENTA + "If you see 'acess denied' message, try rebooting into bootloader")
        except:
            print('An error has occured')
    elif cmd == "unlock":
        try:
            try: code = cmd.split(" ")[1]; device = adb.device(); device.shell('reboot bootloader'); print(Fore.BLUE + device.shell('fastboot oem unlock ' + code))
            except: device = adb.device(); device.shell('reboot bootloader'); print(Fore.BLUE + device.shell('fastboot oem unlock'))
            print(Fore.GREEN + "Done!")
        except:
            print('An error has occured')
    elif cmd == "backup":
        try:
            device = adb.device()
            print(Fore.BLUE + device.shell('backup –apk –shared –all –f backup/backup.ab'))
        except:
            print('An error has occured')
    elif cmd == "restore":
        try:
            device = adb.device()
            print(Fore.BLUE + device.shell('restore /backup/backup.ab'))
        except:
            print('An error has occured')
    elif cmd == "readme":
        print(f"""
{Fore.LIGHTMAGENTA_EX}Credits: {rainbowtext.text("DivineSoftware")}{Fore.GREEN}
{Fore.LIGHTMAGENTA_EX}License: {rainbowtext.text("Attribution-NonCommercial-Share Alike 4.0 International")}
        """)
    elif cmd == "shell":
        try:
            device = adb.device()
            while True:
                shcmd = input(Fore.LIGHTBLUE_EX + device.prop.model + "/ ")
                output = device.shell(shcmd)
                if shcmd == "exit":
                    break
                elif shcmd == "":
                    pass
                else:
                    print(Fore.BLUE + output)
        except:
            print(Fore.RED + "An error has occured")
    elif cmd.find("method") != -1:
        method = cmd.split(" ")[1]
        if method=="1":
            try:
                device = adb.device()
                print(Fore.GREEN + 'Downloading required files...')
                os.system('curl http://supersuroot.org/downloads/supersu-pro.apk -o Superuser.apk')
                os.system('curl https://www.busybox.net/downloads/binaries/1.31.0-i686-uclibc/busybox -o busybox')
                print(Fore.GREEN + 'Rooting...')
                print(Fore.BLUE + device.shell('push su /system/bin'))
                print(Fore.BLUE + device.shell('push busybox /system/bin'))
                print(Fore.BLUE + device.shell('push Superuser.apk /system/app'))
                print(Fore.BLUE + device.shell('chmod 7655 /system/bin/su'))
                print(Fore.BLUE + device.shell('chmod 755 /system/bin/busybox'))
                print(Fore.BLUE + device.shell('chmod 644 /system/app/Superuser.apk'))
                print(Fore.BLUE + device.shell('chown root:shell /system/bin/su'))
                print(Fore.BLUE + device.shell('chown root:shell /system/bin/busybox'))
                print(Fore.BLUE + device.shell('chown root:shell /system/app/Superuser.apk'))
                #device.remove()
                print(Fore.GREEN +  "Device rooted!")
                print(Fore.MAGENTA + "If you see 'acess denied' message, try rebooting into bootloader")
            except:
                print(Fore.RED + "Failed!")
        elif method=="2":
            try:
                device = adb.device()
                print(Fore.GREEN + 'Downloading required files...')
                os.system('curl https://download.chainfire.eu/696/SuperSU/UPDATE-SuperSU-v2.46.zip?retrieve_file=1 -o Supersu.zip')
                print(Fore.GREEN + 'Rooting...')
                print(Fore.BLUE + device.shell('reboot bootloader'))
                print(Fore.BLUE + device.shell('sideload Supersu.zip'))
                #device.remove()
                print(Fore.GREEN + "Device rooted!")
            except:
                print(Fore.RED + "Failed!")
    elif cmd=="help":
        print(logo)
    elif cmd=="exit":
        exit(0)
