import os
import sys
import subprocess
from shutil import which

#-----global var----

#----Check for script root priv

rootCheck = os.geteuid()

if rootCheck != 0:
    print("Need to be run as root user")
    print("Program now exiting")
    exit()


#-----flashrom commands-----
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

#-----open files----
cpuInfo = open("/proc/cpuinfo")
cpuInfo = cpuInfo.read()

uVersion = open("/etc/lsb-release")
uVersion = uVersion.read()

pathCheck = "/sys/firmware/efi"
pathCheck = os.path.isdir(pathCheck)

#-----Terminal commands----
dmiCmd = "dmidecode"
dmiCheck = str(subprocess.check_output(dmiCmd, shell=True))

macAddress = "ip address"
macCheck = str(subprocess.check_output(macAddress, shell=True))

#-----checks dmidecode for device name-----
def checkDmi():

    if "Protectli" in dmiCheck:
        print("\nDevice: Protectli")
        return True

    else:
        print("Device: Unknown")
        return False


#-----checks CPU info using cpuinfo file and dmidecode-----
def chkCpuInfo():


    if "J3060" in cpuInfo and "FW2B" in dmiCheck and "00:e0:67" in macCheck:

        print("Device: FW2B")
        return True

    elif "J3160" in cpuInfo and "FW4B" in dmiCheck and "00:e0:67" in macCheck:

        print("Device: FW4B")
        return True

    elif "3865U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        print("Device: FW6A")
        return True

    elif "7100U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        print("Device: FW6B")
        return True

    elif "7200U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        print("Device: FW6C")
        return True

    else:

        print("Device: Unknownz")
        return False


#-----returns model-----
def cpuInfoPass():

    if "J3060" in cpuInfo and "FW2B" in dmiCheck and "00:e0:67" in macCheck:

        return "FW2B"

    elif "J3160" in cpuInfo  and "FW4B" in dmiCheck and "00:e0:67" in macCheck:

        return "FW4B"

    elif "3865U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        return "FW6x"

    elif "7100U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        return "FW6x"

    elif "7200U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        return "FW6x"

    else:

        return "empty"


#-----checks ubuntu version with lsb-release file-----
def ubuVersion():

    if "20.04" in uVersion:
        print("Ubuntu version: 20.04")
        return True

    elif "18.04" in uVersion:
        print("Ubuntu version: 18.04")
        return True

    else:
        print("Ubuntu version: Unknown")
        return False


#-----check if ubuntu is in legacy or UEFI/ ref path of efi-----
def checkLegacy():

    #if path exists, UEFI
    if not pathCheck:
        print("Ubuntu: Legacy")
        return True

    else:
        print("Ubuntu: UEFI")
        return False

#-----get necessary files/ programs-----
def getNess():

    if which("flashrom"):
        return True

    else:

        os.system("apt-get -y install flashrom")
        #os.system("sudo -S apt-get -y install git")
        #os.system("git clone https://github.com/foxlipro/liflash")

#----- coreboot flash-----

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
        print("Unable to flash coreboot BIOS, system not compatible")

#-----AMI flash------

def flashAMI(passModel):

    if passModel== "FW2B":
        print("\nFlashing AMI for FW2B\n")

        os.system(fw2bami)

    elif passModel == "FW4B":
        print("\nFlashing AMI for FW4B\n")

        os.system(fw4bami)

    elif passModel == "FW6x":
        print("\nFlashing AMI for FW6A/B/C\n")

        os.system(fw6ami)

    else:
        print("Unable to flash AMI BIOS, system not compatible")


##_____MAIN GLOBAL EXE______________________________________________________________________

os.system("clear")

print("\t----LiFlash----")
try:

	if checkDmi() and chkCpuInfo() and ubuVersion() and checkLegacy():
	    print("\nDevice compatible\nProceding with flashing")

	    print("\nobtaining Files")

	    getNess()

	    selection = "-1"

	    while not (selection == "1" or selection == "2"):

	        selection = str(input("1. coreboot\n2. AMI\n"))

	        if selection == "1":
	            flashCoreboot(cpuInfoPass())
	            
        	elif selection == "2":
            	    flashAMI(cpuInfoPass())

        	else:
            	    print("\nPlease enter 1 for coreboot or 2 for AMI")

	else:
    	    print("Device Incompatible Cannot Continue")

except:
	print("Error has occured")
	print("Exiting program")
	exit()
#
