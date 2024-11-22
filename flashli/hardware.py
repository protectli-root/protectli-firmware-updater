"""Hardware interactions."""
from curses import flash
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

def has_param(debugmode: str, param_check) -> bool:
    """Check for a specific parameter

    Args:
        debugmode: Passed parameter if we are emulating a device.

    Returns:
        bool: True if the device has the parameter
    """

    dmi_path = str(subprocess.check_output(['which', 'dmidecode'], shell=False).decode('utf-8')).replace('\n','')
    syscall = subprocess.check_output([dmi_path], shell=False).decode('utf-8') 

    if isinstance(param_check, (set, tuple, list, dict) ):

        for ele in param_check:

            if ele in str(syscall):
                return True

    elif param_check in str(syscall):
        return True

    return False

def get_cpu_data (debugmode: str) -> str:
    
    try:
        cpu_data = subprocess.check_output(['/bin/cat', '/proc/cpuinfo'], stderr=subprocess.DEVNULL).decode('utf-8')  # noqa:S603
    except subprocess.CalledProcessError as exception:
        print('No CPU information found... am I running in a VM or chroot?')
        raise SystemExit('/bin/cat returned error code {0}'.format(exception.returncode))
    
    return cpu_data

def get_cpu(debugmode: str) -> str:
    """Get the CPU model.

    Args:
        debugmode: Passed if this is a debug device.

    Raises:
        SystemExit: If no CPU info is found.

    Returns:
        str: CPU identifier
    """
    cpu_data = get_cpu_data(debugmode)

    cpu_str = re.search(r'model name(\t|\s|:)*(.+)\n', cpu_data).group(2)

    return cpu_str

def get_cpu_step(debugmode: int) -> int:
     """Get the CPU step.

    Args:
        debugmode: Passed if this is a debug device.

    Raises:
        SystemExit: If no CPU info is found.

    Returns:
        int: CPU step
    """
     
     cpu_data = get_cpu_data(debugmode)
     cpu_str = re.search(r'stepping(\t|\s|:)*(.+)\n', cpu_data).group(2)

     return int(cpu_str)

def get_meminfo_total():
    meminfo = subprocess.check_output(['/bin/cat', '/proc/meminfo'], stderr=subprocess.DEVNULL).decode('utf-8')
    meminfo = meminfo.splitlines()[0]

    totalmem = ''

    for char in meminfo:
        if char.isdigit():
            totalmem = totalmem + char 
    
    return int(totalmem)


def get_number_network_ports() -> int:

    all_interfaces = subprocess.check_output(['ls', '/sys/class/net'], text=True).split()

    nic_port_interfaces = []
    for interface in all_interfaces:

        if interface.startswith('enp') or interface.startswith('eno'):

            nic_port_interfaces.append(interface)

    return len(nic_port_interfaces)


def get_protectli_device(debugmode: str, mac_check: str) -> str:
    """Get the model name of this Protectli device.

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        str: Protectli device model name
    """
  
    cpu = get_cpu(debugmode)
    interfaces = get_number_network_ports()

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

    if '10810U' in cpu and get_cpu_step(debugmode) == 1:
        return "vp4670[s1]"
    
    if has_param(debugmode, 'V1210'):

        if interfaces == 2:
            return 'v1210'

        elif interfaces == 4:
            return 'v1410'
        
        else:
            return 'Unknown'
    
    if has_param(debugmode, 'V1211'):

        # meminfo = get_meminfo_total()
        # if meminfo in [7905332, 8006576]:

        return 'v1211'

    if has_param(debugmode, 'V1410'):

        if interfaces == 2:
            return 'v1210'

        elif interfaces == 4:
            return 'v1410'
        
        else:
            return 'Unknown'

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

    device_mac = 0

    address_dir = ['/sys/class/net/enp1s0f0/address',
                   '/sys/class/net/enp2s0f0/address',
                   '/sys/class/net/eno1/address',
                   '/sys/class/net/enp1s0/address',
                   '/sys/class/net/enp2s0/address',
                   '/sys/class/net/enp4s0/address',
                   '/sys/class/net/enp5s0/address',
                   ]
    
    for add_dir in address_dir :
        if os.path.isfile(add_dir):
            device_mac = str(subprocess.check_output(['/bin/cat', add_dir], shell=False).decode('utf-8'))
            break
             
    if not device_mac:
        return False
    
    else:
        return device_mac


def check_bios_lock (debugmode: str) -> str:
    """Runs flashrom to check for errors.

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        bool
    """

    if (has_param('null',['VP2420', 'VP6630', 'VP6650', 'VP6670'])) :
        flashrom_dir = './vendor/flashrom_v2'
    
    else :
        flashrom_dir = './vendor/flashrom'
    
    flashrom_status = str(subprocess.run([flashrom_dir, '-p', 'internal'], capture_output=True))

    # Flashrom error for AMI
    if 'Warning: BIOS region SMM protection is enabled!' in flashrom_status:

        return True
        
    # Flashrom error for coreboot
    elif 'PR0: Warning:' in flashrom_status:

        read_only_addresses = {'0x00c00000-0x00ffffff',
                               '0x00b80000-0x00ffffff',
                               }

        for address in read_only_addresses:
            if (address + ' is read-only') in flashrom_status:
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

def check_secureboot(debugmode):
    """Checks if BIOS is coreboot

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        bool
    """
    mokutil_check = str(subprocess.run(['which', 'mokutil'], capture_output=True))
    secureboot_status = str(subprocess.run(['mokutil', '--sb-state'], capture_output=True))

    if mokutil_check:

        if 'enabled' in secureboot_status:
            return True
        
        elif 'disabled' in secureboot_status:
            return False
    else:

        print('\nUnable to locate mokutil\n')
        return False
