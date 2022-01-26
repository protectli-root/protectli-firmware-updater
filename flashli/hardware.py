"""Hardware interactions."""
import os
import re
import subprocess  # noqa:S404

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
    return re.search(r'model name(\t|\s|:)*(.+)\n', cpu_data).group(2)


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
        device = 'vp2410'
        return device

    if mac_check == 'vp_vr2':
        device = 'vp2410r'
        return device

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

