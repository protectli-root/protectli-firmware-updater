"""Hardware interactions."""
from curses import flash
from nis import match
import os
import re
import subprocess

#from click import argument  # noqa:S404

from flashli import configurations

def is_protectli_device(debugmode: str) -> bool:
    """Detect if this is a Protectli device.

    Args:
        debugmode: Passed parameter if we are emulating a device.

    Returns:
        bool: True if this is a Protectli device
    """
    dmi_path = str(subprocess.check_output(['which', 'dmidecode'], shell=False).decode('utf-8')).replace('\n','')

    syscall = subprocess.check_output([dmi_path], shell=False).decode('utf-8')  # noqa:S603
    match1 = 'Protectli' in str(syscall)
    match2 = 'YANLING' in str(syscall)
    return match1 or match2 or debugmode

def has_param(debugmode: str, param_check: str) -> bool:
    """Check for a specific parameter

    Args:
        debugmode: Passed parameter if we are emulating a device.

    Returns:
        bool: True if the device has the parameter
    """
    dmi_path = str(subprocess.check_output(['which', 'dmidecode'], shell=False).decode('utf-8')).replace('\n','')
    syscall = subprocess.check_output([dmi_path], shell=False).decode('utf-8') 

    if param_check in str(syscall):
        return True

    return False



def get_cpu(debugmode: str) -> str:
    """Get the CPU model.

    Args:
        debugmode: Passed if this is a debug device.

    Raises:
        SystemExit: If no CPU info is found.

    Returns:
        str: CPU identifier
    """
    cpu_data = ''
    try:
        cpu_data = subprocess.check_output(['/bin/cat', '/proc/cpuinfo'], stderr=subprocess.DEVNULL).decode('utf-8')  # noqa:S603
    except subprocess.CalledProcessError as exception:
        print('No CPU information found... am I running in a VM or chroot?')
        raise SystemExit('/bin/cat returned error code {0}'.format(exception.returncode)) 
    cpu_str = re.search(r'model name(\t|\s|:)*(.+)\n', cpu_data).group(2)

    return cpu_str



def get_protectli_device(debugmode: str, mac_check: str) -> str:
    """Get the model name of this Protectli device.

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        str: Protectli device model name
    """
    if debugmode:
        return debugmode
        
    cpu = get_cpu(debugmode)

    if mac_check == 'vp_vr1':
        return 'vp2410'

    if mac_check == 'vp_vr2':
        return 'vp2410r'

    if cpu == '3867U':
        return "fw6ar"

    if cpu == '7020U':
        return 'fw6br'

    if cpu == '8130U':
        return 'fw6br2'
    
    if '3865U' in cpu or '7100U' in cpu or '7200U' in cpu and get_nicTest(debugmode):
        return "fw6m"

    for device, props in configurations.CONFIGURATIONS.items():
        if props['cpu'] in cpu:
            return '{0}'.format(device) 
            
    return 'Unknown'


def get_bios_mode(debugmode: str) -> str:
    """Check if currently running in EFI or BIOS mode.

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        str: BIOS mode
    """
    if debugmode:
        return 'BIOS'
    if os.path.isdir('/sys/firmware/efi'):
        return 'EFI'

    return 'BIOS'

def get_nicTest(debugmode: bool) -> bool:

    """Checks if 82583 is present

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
         bool
    """

    pci_list = str(subprocess.check_output(['lspci'], shell=False).decode('utf-8'))

    if "82583" in pci_list:
        return True

    return False

def get_mac(debugmode: str) -> str:
    """Checks the first NIC for mac

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
         str: NIC mac
    """
    vp2410_mac_dir = '/sys/class/net/eno1/address'
    other_unites_mac_dir = '/sys/class/net/enp1s0/address'

    if os.path.isfile(vp2410_mac_dir):

        device_mac = str(subprocess.check_output(['/bin/cat', vp2410_mac_dir], shell=False).decode('utf-8'))

    else:

        device_mac = str(subprocess.check_output(['/bin/cat', other_unites_mac_dir], shell=False).decode('utf-8'))

    return device_mac

def check_bios_lock (debugmode: str) -> str:
    """Runs flashrom to check for errors.

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        bool
    """
    flashrom_dir = './vendor/flashrom'
    flashrom_status = str(subprocess.run([flashrom_dir, '-p', 'internal'], capture_output=True))

    # Flashrom error for AMI
    if 'Warning: BIOS region SMM protection is enabled!' in flashrom_status:

        return True
        
    # Flashrom error for coreboot
    elif 'PR0: Warning: 0x00c00000-0x00ffffff is read-only' in flashrom_status:

        return True
        
    else:
        return False

def check_for_ami(debugmode):
    """Checks if BIOS is AMI

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        bool
    """

    if has_param(debugmode, 'American Megatrends'):
        return True
    
    return False

def check_for_coreboot(debugmode):
    """Checks if BIOS is coreboot

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        bool
    """

    if has_param(debugmode, 'coreboot'):
        return True
    
    return False
