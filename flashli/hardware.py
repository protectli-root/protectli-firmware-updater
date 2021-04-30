"""Hardware interactions."""
import os
import re
import subprocess  # noqa:S404


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
    global DEBUGMODE
    if DEBUGMODE:
        return DEBUGMODE
    cpu = get_cpu()
    global CONFIGURATIONS
    for device, props in CONFIGURATIONS.items():
        if props['cpu'] in cpu:
            return device
    return 'Unknown model'


def get_bios_mode() -> str:
    """Check if currently running in EFI or BIOS mode.

    Returns:
        str: BIOS mode
    """
    return 'EFI' if os.path.isdir('/sys/firmware/efi') else 'BIOS'
