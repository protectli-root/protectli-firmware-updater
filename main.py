#!/usr/bin/env python3

"""Protectli device BIOS flasher.

This tool will flash new BIOS onto the machine that runs this script.
"""

import os
import re
import subprocess  # noqa:S404

from configurations import CONFIGURATIONS

configurations = CONFIGURATIONS

VERSION = '1.1.0'

# Set a debug hardware here.
DEBUGMODE = ''

if os.geteuid() != 0 and not DEBUGMODE:
    print('Need to be run as root user')
    print('Please run: sudo ./main.py')
    print('Program now exiting.')
    exit()


def get_version() -> str:
    """Functional way to get global VERSION.

    Returns:
        str: Value of global VERSION
    """
    global VERSION
    return VERSION


def get_terminal_width() -> int:
    """Get the width of the current terminal in characters.

    Returns:
        int: Width in characters
    """
    return os.get_terminal_size().columns


def is_protectli_device() -> bool:
    """Detect if this is a Protectli device.

    Returns:
        bool: True if this is a Protectli device
    """
    cmd = '/usr/sbin/dmidecode'
    syscall = subprocess.check_output([cmd], shell=False).decode('utf-8')  # noqa:S603
    match1 = 'Protectli' in str(syscall)
    match2 = 'YANLING' in str(syscall)
    global DEBUGMODE
    return match1 or match2 or DEBUGMODE


def get_cpu() -> str:
    """Get the CPU model.

    Returns:
        str: CPU identifier
    """
    cpu_data = subprocess.check_output(['/bin/cat', '/proc/cpuinfo']).decode('utf-8')  # noqa:S603
    return re.search(r'model name(\t|\s|:)*(.+)\n', cpu_data).group(2)


def get_protectli_device() -> str:
    """Get the model name of this Protectli device.

    Returns:
        str: Protectli device model name
    """
    global configurations
    global DEBUGMODE
    cpu = get_cpu()
    if DEBUGMODE:
        return DEBUGMODE
    for device, props in configurations.items():
        if props['cpu'] in cpu:
            return device
    return 'Unknown model'


def get_bios_mode() -> str:
    """Check if currently running in EFI or BIOS mode.

    Returns:
        str: BIOS mode
    """
    return 'EFI' if os.path.isdir('/sys/firmware/efi') else 'BIOS'


def get_image_path(model: str, requested_bios: str) -> str:
    """Get path to BIOS image.

    Args:
        model: Protectli device model name
        requested_bios: The BIOS to be located

    Returns:
        str: Path to the BIOS file requested
    """
    global configurations
    for bios in configurations[model]['bios']:
        if bios['vendor'] == requested_bios:
            return 'images/{0}'.format(bios['file'])


def do_flash(model: str, bios: str):
    """Perform the BIOS flash.

    Args:
        model: Protectli device model name
        bios: The BIOS to be flashed
    """
    global DEBUGMODE
    if DEBUGMODE:
        print('Not actually flashing, script is in debug mode.')
        return
    file_path = get_image_path(model, bios)
    subprocess.run('vendor/flashrom -p internal -w {0} --ifd -i bios'.format(file_path))  # noqa:S603


def print_supported_products():
    """Get list of devices from Configurations and prints to STDOUT."""
    global configurations
    devices = list(map(lambda dev: dev.upper(), list(configurations)))
    devices.sort()
    print(*devices, sep='\n')


def get_user_selection(device: str):
    """Get BIOS selection from user based on available images for device.

    Args:
        device: Which device to ask the user about

    Returns:
        str: Vendor name
    """
    global configurations
    available_options = configurations[device]['bios']
    selection = ''
    while selection not in map(lambda option: option['vendor'], available_options):
        number = 1
        for available_option in available_options:
            print('{0}: {1}'.format(str(number), available_option['vendor']))
            number += 1
        user_input = int(input())
        if (0 < user_input <= len(available_options)):
            return available_options[user_input - 1]['vendor']


def main():  # noqa:WPS213
    """Main program."""
    device = get_protectli_device()
    os.system('/bin/clear')  # noqa:S607,S605
    print('FlashLi'.center(get_terminal_width(), '='))
    print('--Version {0}--'.format(get_version()).center(get_terminal_width(), '-'))

    print('Device: {0}'.format(device))
    if not is_protectli_device():
        print('Sorry, this is an unsupported device.')
        print('This tool is used to flash BIOS onto the following Protectli products:')
        print_supported_products()
        quit()

    print('BIOS Mode: {0}'.format(get_bios_mode()))
    print('Available BIOS:')

    selection = get_user_selection()

    do_flash(device, selection)
    print('Make sure the flash has been VERIFIED')
    print('If the flash has not been VERIFIED please run the script again')
    print('-If the flash is VERIFIED please restart the device')


main()
