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
    cmd = '/usr/sbin/dmidecode'
    syscall = subprocess.check_output([cmd], shell=False).decode('utf-8')  # noqa:S603
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


def get_protectli_device(debugmode: str) -> str:
    """Get the model name of this Protectli device.

    Args:
        debugmode: Passed if this is a debug device.

    Returns:
        str: Protectli device model name
    """
    if debugmode:
        return debugmode
    cpu = get_cpu(debugmode)

    for device, props in configurations.CONFIGURATIONS.items():
        if props['cpu'] in cpu:
            return '{0}'.format(device)
    return 'Unknown device'


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
