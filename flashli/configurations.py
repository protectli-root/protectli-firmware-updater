"""Hardware configuration dict."""

import types

CONFIGURATIONS = types.MappingProxyType({
    'fw2': {
        'cpu': 'J1800',
        'bios': [
            {
                'vendor': 'ami',
                'file': '',
            },
        ],
    },
    'fw2b': {
        'cpu': 'J3060',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW2_BSW4L009.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw2b_v4.9.0.1.rom',
            },
        ],
    },
    'fw1': {
        'cpu': 'J1900',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW2_BSW4L009.bin',
            },
        ],
    },
    'fw4a': {
        'cpu': 'E3845',
        'bios': [
            {
                'vendor': 'ami',
                'file': '',
            },
        ],
    },
    'fw4b': {
        'cpu': 'J3160',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW4_BSW4L009.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw4b_v4.12.0.3.rom',
            },
        ],
    },
    'fw6a': {
        'cpu': '3865U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw6_v4.12.0.3.rom',
            },
        ],
    },
    'fw6b': {
        'cpu': '7100U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw6_v4.12.0.3.rom',
            },
        ],
    },
    'fw6c': {
        'cpu': '7200U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw6_v4.12.0.3.rom',
            },
        ],
    },
    'fw6d': {
        'cpu': '8250U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
        ],
    },
    'fw6e': {
        'cpu': '8550U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW6_KBU6LA09.bin',
            },
        ],
    },
    'vp2410': {
        'cpu': 'J4125',
        'bios': [
            {
                'vendor': 'amitest',
                'file': 'VP2410_GLK34L250.bin',
            },
        ],
    },
})
