#!/usr/bin/env python3

import os
import sys
import subprocess
from shutil import which

from colorama import Fore, Style

# -----global var----

menFact = ""
deviceName = ""
ubVersion = ""
biosVers = ""
flashFileCore = "none"
flashFileAmi = "none"

over_ride_tester = True

# ----Check for script root priv

rootCheck = os.geteuid()

if rootCheck != 0:
    print(Fore.RED + "\nNeed to be run as root user" + Style.RESET_ALL)
    print(Fore.YELLOW + "Please run: sudo python3 main.py" + Style.RESET_ALL)
    print(Fore.RED + "\nProgram now exiting\n" + Style.RESET_ALL)
    exit()

# -----flashrom commands-----
fw2bRomFile = "images/protectli_fw2b_v4.12.0.3.rom"
fw4bRomFile = "images/protectli_fw4b_v4.12.0.3.rom"
fw6RomFile = "images/protectli_fw6_v4.12.0.3.rom"

fw2bBinFile = "images/FW2_BSW4L009.bin"
fw4bBinFile = "images/FW4_BSW4L009.bin"
fw6BinFile = "images/FW6_KBU6LA09.bin"

fw2bcoreboot = "flashrom -p internal -w " + fw2bRomFile + " --ifd -i bios"
fw4bcoreboot = "flashrom -p internal -w " + fw4bRomFile + " --ifd -i bios"
fw6coreboot = "flashrom -p internal -w " + fw6RomFile + " --ifd -i bios"

fw2bami = "flashrom -p internal -w " + fw2bBinFile + " --ifd -i bios"
fw4bami = "flashrom -p internal -w " + fw4bBinFile + " --ifd -i bios"
fw6ami = "flashrom -p internal -w " + fw6BinFile + " --ifd -i bios"

# -----open files----
cpuInfo = open("/proc/cpuinfo")
cpuInfo = cpuInfo.read()

uVersion = open("/etc/lsb-release")
uVersion = uVersion.read()

pathCheck = "/sys/firmware/efi"
pathCheck = os.path.isdir(pathCheck)

# -----Terminal commands----
dmiCmd = "dmidecode"
dmiCheck = str(subprocess.check_output(dmiCmd, shell=True))

macAddress = "ip address"
macCheck = str(subprocess.check_output(macAddress, shell=True))


# -----checks dmidecode for device name-----
def checkDmi():
    global menFact
    if "Protectli" in dmiCheck:
        menFact = "Protectli"

        return True

    else:
        menFact = "Unknown"
        print("Fail at DMI")
        return False


# -----checks CPU info using cpuinfo file and dmidecode-----
def chkCpuInfo():
    global deviceName
    global flashFileCore
    global flashFileAmi

    if "J3060" in cpuInfo and "FW2B" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW2B"
        flashFileCore = fw2bRomFile
        flashFileAmi = fw2bBinFile
        return True

    elif "J3160" in cpuInfo and "FW4B" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW4B"
        flashFileCore = fw4bRomFile
        flashFileAmi = fw4bBinFile
        return True

    elif "3865U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW6A"
        flashFileCore = fw6RomFile
        flashFileAmi = fw6BinFile
        return True

    elif "7100U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW6B"
        flashFileCore = fw6RomFile
        flashFileAmi = fw6BinFile
        return True

    elif "7200U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW6C"
        flashFileCore = fw6RomFile
        flashFileAmi = fw6BinFile
        return True

    elif "8525" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        print(Fore.YELLOW + "\nPlatform is not compatible at the moment\n" + Style.RESET_ALL)
        flashFileCore = "Not selected"
        flashFileAmi = "Not selected"
        return False

    elif "8550" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        print(Fore.YELLOW + "\nFW6E: Platform is not compatible at the moment\n" + Style.RESET_ALL)
        flashFileCore = "Not selected"
        flashFileAmi = "Not selected"
        return False

    else:

        deviceName = "Unknown"
        return False


# -----returns model-----
def cpuInfoPass():
    print("old function")


# -----checks ubuntu version with lsb-release file-----
def ubuVersion():
    global ubVersion

    if "20.10" in ubVersion:
        ubVersion = "20.10"
        return True

    elif "20.04" in uVersion:
        ubVersion = "20.04"
        return True

    elif "18.04" in uVersion:
        ubVersion = "18.04"
        return True

    else:
        ubVersion = "Unknown"
        print("Fail at U1")
        return False


# -----check if ubuntu is in legacy or UEFI/ ref path of efi-----
def checkLegacy():
    global biosVers
    # if path exists, UEFI
    if not pathCheck:
        biosVers = "Legacy"
        return True

    else:
        biosVers = "UEFI"
        print("Fail at bio")
        return False


# -----get necessary files/ programs-----
def getNess():
    if which("flashrom"):

        print(Fore.GREEN + "Flashrom has been found\n" + Style.RESET_ALL)

        return True

    else:
        select_to_install = "x"
        print("Flashrom is not is not installed")
        print("Flashrom is required to be able to flash to coreboot")
        print("Would you like to install flashrom [Y/N]\n")

        while not (select_to_install == "Y" or select_to_install == "N"):

            select_to_install = str(input("")).upper()

            if select_to_install == "Y":

                print(Fore.GREEN + "\nProceeding with installing flashrom, please wait\n" + Style.RESET_ALL)
                os.system("apt-get -y install flashrom")

                if which("flashrom"):

                    print(Fore.GREEN + "\nflashrom has been successfully installed\nproceeding with operations\n" + Style.RESET_ALL)

                    return True

                else:

                    print(Fore.RED + "\nflashrom has failed to install")
                    print("Repository might need to be updated")
                    print("Would you like to update a repository and try to install flashrom [Y/N]" + Style.RESET_ALL)
                    user_input = "x"

                    while not (user_input == "Y" or user_input == "N"):

                        user_input =str(input("")).upper()

                        if user_input == "Y":
                            os.system("add-apt-repository universe")
                            os.system("apt-get -y install flashrom")

                            if which("flashrom"):
                                print(Fore.GREEN + "\nFlashrom has been installed" + Style.RESET_ALL)
                                return True

                            else:
                                print(Fore.RED + "Flashrom has fialed to install, Error E30P" + Style.RESET_ALL)
                                return False

                        else:
                            print("\nflashrom is required to continue, program will now exit")
                            exit()

            elif select_to_install == "N":

                print(Fore.RED + "\nflashrom is required to continue, program will now exit" + Style.RESET_ALL)

                exit()

            else:
                print("Please enter \"Y\" for Yes and \"N\" for No")

# ----- coreboot flash-----

def flashCoreboot(passModel):
    if passModel == "FW2B":
        print("Flashing coreboot for FW2B")

        os.system(fw2bcoreboot)

    elif passModel == "FW4B":
        print("Flashing coreboot for FW4B")

        os.system(fw4bcoreboot)

    elif passModel == "FW6x":
        print("Flashing coreboot for FW6A/B/C")

        os.system(fw6coreboot)

    else:
        print(Fore.RED + "Unable to flash coreboot BIOS, system not compatible")


# -----AMI flash------

def flashAMI(passModel):
    if passModel == "FW2B":
        print("\nFlashing AMI for FW2B\n")

        os.system(fw2bami)

    elif passModel == "FW4B":
        print("\nFlashing AMI for FW4B\n")

        os.system(fw4bami)

    elif passModel == "FW6x":
        print("\nFlashing AMI for FW6A/B/C\n")

        os.system(fw6ami)

    else:
        print(Fore.RED + "Unable to flash AMI BIOS, system not compatible" + Style.RESET_ALL)


# -----Coreboot or AMI choice
def flasherChoice():
    selection = "-1"

    while not (selection == "1" or selection == "2"):

        selection = str(input("1. coreboot\n2. AMI\n"))

        if selection == "1":
            flashCoreboot(deviceName)

        elif selection == "2":
            flashAMI(deviceName)

        else:
            print("\nPlease enter 1 for coreboot or 2 for AMI")


# -----Full System Check

def fullSysChk():
    if checkDmi() and chkCpuInfo() and ubuVersion() and checkLegacy():

        return True

    else:
        print("Fail at Full system check")
        return False


# -----Menu------

def displayInfo():
    print("\t----FlashLi----\n")

    print("\t--Pawn: 2A3--\n")

    print("Manufacture: " + menFact)
    print("Device: " + deviceName)
    print("Ubuntu version: " + ubVersion)
    print("OS: " + biosVers)

    print(Fore.YELLOW + "\nFlash file used for coreboot: " + flashFileCore)
    print("Flash file used for AMI: " + flashFileAmi + Style.RESET_ALL)
    print("\n")


##_____MAIN EXE______________________________________________________________________

os.system("clear")

# initialize the check system process
checkDmi()
chkCpuInfo()
ubuVersion()
checkLegacy()

# trying to execute the main scrip application
try:

    if fullSysChk():

        if getNess():

            displayInfo()
            flasherChoice()

            print(Fore.YELLOW + "\n\n-Make sure the flash has been VERIFIED")
            print("-If the flash has not been VERIFIED please run the script again")
            print("-If the flash is VERIFIED please restart the device" + Style.RESET_ALL)

        else:
            print(Fore.RED + "Installing Flashrom was not successful")

    else:

        print(Fore.RED + "\nPlatform is not compatible with flashing the specific BIOS\n" + Style.RESET_ALL)



except:
    print(Fore.RED + "\nError has occurred")
    print("Exiting program" + Style.RESET_ALL)

    exit()
#
