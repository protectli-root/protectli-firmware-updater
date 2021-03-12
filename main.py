import os
import sys
import subprocess
from shutil import which

#-----global var----

menFact = ""
deviceName = ""
ubVersion = ""
biosVers = ""

over_ride_tester = True

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

    global menFact
    if "Protectli" in dmiCheck:
        menFact = "Protectli"
        return True

    else:
        menFact = "Unknown"
        return False


#-----checks CPU info using cpuinfo file and dmidecode-----
def chkCpuInfo():

    global deviceName

    if "J3060" in cpuInfo and "FW2B" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW2B"
        return True

    elif "J3160" in cpuInfo and "FW4B" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW4B"
        return True

    elif "3865U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW6A"
        return True

    elif "7100U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW6B"
        return True

    elif "7200U" in cpuInfo and "FW6" in dmiCheck and "00:e0:67" in macCheck:

        deviceName = "FW6C"
        return True

    else:

        deviceName = "Unknown"
        return False


#-----returns model-----
def cpuInfoPass():

    print("old function")


#-----checks ubuntu version with lsb-release file-----
def ubuVersion():

    global ubVersion

    if "20.04" in uVersion:
        ubVersion = "20.04"
        return True

    elif "18.04" in uVersion:
        ubVersion = "18.04"
        return True

    else:
        ubVersion = "Unknown"
        return False


#-----check if ubuntu is in legacy or UEFI/ ref path of efi-----
def checkLegacy():

    global biosVers
    #if path exists, UEFI
    if not pathCheck:
        biosVers = "Legacy"
        return True

    else:
        biosVers = "UEFI"
        return False

#-----get necessary files/ programs-----
def getNess():


    if which("flashrom"):
        return True

    else:
        select_to_install = "x"
        print("Flashrom is not is not installed")
        print("Flashrom is required to be able to flash to coreboot")
        print("Would you like to install flashrom [Y/N]\n")

        while not(select_to_install == "Y" or select_to_install == "N"):

            select_to_install = str(input("")).upper()

            if select_to_install == "Y":

                print("\nProceeding with installing flashrom, please wait\n")
                os.system("apt-get -y install flashrom")

                if which("flashrom"):

                    print("\nflashrom has been successfully installed\nproceeding with operations\n")

                    return True

                else:

                    print("\nflashrom has failed to install\nplease check internet connection")
                    getNess()

            elif select_to_install == "N":

                print("\nflashrom is required to continue, program will now exit")

                exit()

            else:
                print("Please enter \"Y\" for Yes and \"N\" for No")


        #os.system("apt-get -y install flashrom")
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

#-----Coreboot or AMI choice
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


#-----Full System Check

def fullSysChk():

    if checkDmi() and chkCpuInfo() and ubuVersion() and checkLegacy():

        return True

    else:

        return False

#-----Menu------

def menu():

    print("\t----FlashLi----\n")

    print("Manufacture: " + menFact)
    print("Device: " + deviceName)
    print("Ubuntu version: " + ubVersion)
    print("OS: " + biosVers)
    print("\n")


##_____MAIN GLOBAL EXE______________________________________________________________________

os.system("clear")

checkDmi()
chkCpuInfo()
ubuVersion()
checkLegacy()


try:

    if over_ride_tester:


    #if checkDmi() and chkCpuInfo() and ubuVersion() and checkLegacy():
        #print("\nDevice compatible\nProceding with flashing")

        #print("\nobtaining Files")

        if getNess():

            menu()
            flasherChoice()

        else:
            print("installing Flashrom was not successful")

    else:

        print("platfrom is not compatible")



except:
    print("Error has occured")
    print("Exiting program")
    exit()
#
