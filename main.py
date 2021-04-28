#!/usr/bin/env python3

import os
import sys
import subprocess

debugMode = ''

if os.geteuid() != 0:
    print("\nNeed to be run as root user")
    print("Please run: sudo python3 main.py")
    print("\nProgram now exiting\n")
    exit()

configurations = {
    'fw2': {
        'cpu': 'J1800',
        'bios': [
            {
                'name': 'ami',
                'file': '',
            },
        ],
    },
    'fw2b': {
        'cpu': 'J3060',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW2_BSW4L009.bin',
            },
            {
                'name': 'coreboot',
                'file': 'protectli_fw2b_v4.9.0.1.rom',
            },
        ],
    },
    'fw1': {
        'cpu': 'J1900',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW2_BSW4L009.bin',
            },
        ],
    },
    'fw4a': {
        'cpu': 'E3845',
        'bios': [
            {
                'name': 'ami',
                'file': '',
            },
        ],
    },
    'fw4b': {
        'cpu': 'J3160',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW4_BSW4L009.bin',
            },
            {
                'name': 'coreboot',
                'file': 'protectli_fw4b_v4.12.0.3.rom'
            },
        ],
    },
    'fw6a': {
        'cpu': '3865U',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
            {
                'name': 'coreboot',
                'file': 'protectli_fw6_v4.12.0.3.rom'
            },
        ],
    },
    'fw6b': {
        'cpu': '7100U',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
            {
                'name': 'coreboot',
                'file': 'protectli_fw6_v4.12.0.3.rom'
            },
        ],
    },
    'fw6c': {
        'cpu': '7200U',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
            {
                'name': 'coreboot',
                'file': 'protectli_fw6_v4.12.0.3.rom'
            },
        ],
    },
    'fw6d': {
        'cpu': '8250U',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
        ],
    },
    'fw6e': {
        'cpu': '8550U',
        'bios': [
            {
                'name': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
        ],
    },
    'vp2410': {
        'cpu': 'J4125',
        'bios': [
            {
                'name': 'amitest',
                'file': 'VP2410_GLK34L250.bin',
            },
        ],
    },
}

def is_protectli_device():
    """Detect if this is a Protectli device.

    Returns:
        Returns True if this is a Protectli device.
    """
    syscall = subprocess.check_output(['/usr/sbin/dmidecode'], shell=False)
    match1 = 'Protectli' in str(syscall)
    match2 = 'YANLING' in str(syscall)
    return match1 or match2

def get_cpu():
    return subprocess.check_output('cat /proc/cpuinfo | grep -i "^model name" | uniq', shell=True).decode('utf-8')


def get_protectli_device():
    """Get the model name of this Protectli device.

    Returns:
        Returns Protectli device model name as a string.
    """
    global configurations
    global debugMode
    if debugMode:
        return debugMode
    cpu = get_cpu()
    for k, v in configurations.items():
        if v['cpu'] in cpu:
            return k
    return 'Unknown model'


def isUEFI():
    """Check if currently running in EFI mode.

    Returns:
        Boolean
    """
    pathCheck = "/sys/firmware/efi"
    return os.path.isdir(pathCheck)


def get_image_path(model, bios):
    """Get path to BIOS image

    Returns:
        Path to the BIOS file to flash as string
    """
    global configurations
    for v in configurations[model]['bios']:
        if v['name'] == bios:
            return 'images/' + v['file']


def do_flash(model, bios):
    """Perform BIOS flash
    Parameters:

    Returns:
        Void
    """
    filePath = get_image_path(model, bios)
    os.system('flashrom -p internal -w ' + filePath + ' --ifd -i bios')


def main():
    """Main

    Returns:
        Void
    """
    device = get_protectli_device()
    os.system('clear')
    print("\t----FlashLi----\n")
    print("\t--Version 0.1.01--\n")


    print("Device: " + device)
    if not is_protectli_device():
        print("Unsupported device.")
        quit()

    print("BIOS Mode: " + 'EFI' if isUEFI() else 'BIOS')
    print("\n")
    print("Available BIOS:")

    global configurations
    availableOptions = configurations[device]['bios']
    print(availableOptions)

    selection = ''
    while selection not in map(lambda a: a['name'], availableOptions):
        i = 1
        for v in availableOptions:
            print(str(i) + ': ' + v['name'])
            i += 1
        userInput = int(input())
        if (userInput > 0 and userInput <= len(availableOptions)):
            selection = availableOptions[userInput - 1]['name']
            continue

    do_flash(device, selection)
    print("\n\n-Make sure the flash has been VERIFIED")
    print("-If the flash has not been VERIFIED please run the script again")
    print("-If the flash is VERIFIED please restart the device")


main()
#
