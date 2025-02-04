"""Hardware configuration dict."""

import types

flash_command = 'vendor/flashrom -p internal -w {0} --ifd -i bios'
flashli_command_pkfail = 'vendor/flashrom -p internal -w {0}'
overrider_command = 'vendor/flashrom -p internal:boardmismatch=force -w {0} --ifd -i bios'

vp24_vp66_command = 'vendor/flashrom_v2 -p internal -w {0}'
vp2420_upgrade = 'vendor/flashrom_v2 -p internal -w {0} --fmap -i RW_SECTION_A'
alt_upgrade = 'vendor/flashrom_v2 -p internal -w {0} --fmap -i RW_SECTION_A -i WP_RO'

vpxxxx_flash_command = 'vendor/flashrom -p internal -w {0}'
vpxxxx_upgrade = 'vendor/flashrom -p internal -w {0} --fmap -i RW_SECTION_A'

CONFIGURATIONS = types.MappingProxyType({
    'fw2': {
        'cpu': 'J1800',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW2_BTL4A012.bin',
            },
        ],
        'command': flash_command,
    },
    'fw2b': {
        'cpu': 'J3060',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw2b_YLBWL240P.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw2b_v4.9.0.3.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw1': {
        'cpu': 'J1900',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW1_BTL4A012.bin',
            },
        ],
        'command': flash_command,
    },
    'fw4a': {
        'cpu': 'E3845',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'FW4A_E38L4A12.bin',
            },
        ],
        'command': flash_command,
    },
    'fw4b': {
        'cpu': 'J3160',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw4b_YLBWL440P.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw4b_v4.12.0.8.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw4c': {
        'cpu': 'J3710',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw4c_MBSW0104.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_fw4c_v4.12.0.12.rom'
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw6a': {
        'cpu': '3865U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },

    'fw6ar': {
        'cpu': '3867U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw6b': {
        'cpu': '7100U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw6br': {
        'cpu': '7020U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw6br2': {
        'cpu': '8130U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw6c': {
        'cpu': '7200U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
    },
    'fw6m': {
        'cpu': 'FW6MC',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_825_KBU6LA09.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flash_command,
    },
    'fw6d': {
        'cpu': '8250U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
        'override': overrider_command,
    },
    'fw6e': {
        'cpu': '8550U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'fw6_all_YKR6LV30.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_all_fw6_vault_kbl_v1.0.14.rom',
            },
        ],
        'command': flashli_command_pkfail,
        'override': overrider_command,
    },
    'v1210': {
        'cpu': 'N5105',
        'bios': [
            {
                'vendor': 'ami',
                'file' : 'v1210_JPL.2LAN.S4G.PCIE.6W.013.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_v1210_v0.9.3.rom',

            },
        ],
        'command': vp24_vp66_command,
    },
    'v1211': {
        'cpu': 'N5105',
        'bios': [
            {
                'vendor': 'ami',
                'file' : 'v1211_JPL.2LAN.D8G.PCIE.6W.009.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_v1211_v0.9.3.rom',

            },
        ],
        'command': vp24_vp66_command,
    },
    'v1410': {
        'cpu': 'N5105',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'v1410_JPL.4LAN.S8GB.PCIE.6W.007B.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_v1410_v0.9.3.rom',

            },
        ],
        'command': vp24_vp66_command,
    },
    'v1610': {
        'cpu': 'N6005',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'v1610_JPL.6LAN.D16G.PCIE.007.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_v1610_v0.9.3.rom',

            },
        ],
        'command': vp24_vp66_command,
    },
    'vp2410': {
        'cpu': 'J4125',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp2410_GLK4L280.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp2410_DF_1.0.9.rom',

            },
        ],
        'command': vpxxxx_flash_command,
    },
    'vp2410r': {
        'cpu': 'J4125',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp2410_YGM4LV22.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp2410_v1.1.1.rom',
            },
        ],
        'command': vpxxxx_flash_command,
    },
    'vp2420': {
        'cpu': 'J6412',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp2420_YELD4L13P.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp2420_v1.2.0.rom',
            },
        ],
        'command': vp24_vp66_command,
        'upgrade': vp2420_upgrade,
        'alt_upgrade' : alt_upgrade,
    },
    'vp4630': {
        'cpu': '10110U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp4630_v2_YW6L2318.bin',

            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp4600_v1.2.0.rom',
            },

        ],
        'command': vpxxxx_flash_command,
        'upgrade': vpxxxx_upgrade,
    },
     'vp4650': {
        'cpu': '10210U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp4650_v2_YW6L2518.bin',
                
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp4600_v1.2.0.rom',
                
            },

        ],
        'command': vpxxxx_flash_command,
        'upgrade': vpxxxx_upgrade,
    },
    'vp4670': {
        'cpu': '10810U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp4670_v1_YW6L1717.bin',
                
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp4600_v1.2.0.rom',
                
            },

        ],
        'command': vpxxxx_flash_command,
        'upgrade': vpxxxx_upgrade,
        'alt_upgrade' : alt_upgrade,
    },
    'vp4670[s1]': {
        'cpu': '10810U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp4670_v2_YW6L2722.bin',
                
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp4600_v1.2.0.rom',
                
            },

        ],
        'command': vpxxxx_flash_command,
        'upgrade': vpxxxx_upgrade,
        'alt_upgrade' : alt_upgrade,
    },
    'vp6630': {
        'cpu': '1215U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp6630_ADZ6L314.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp6600_v0.9.1.rom',
            },

        ],
        'command': vp24_vp66_command,

    },
    'vp6650': {
        'cpu': '1235U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp6650_ADZ6L514.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp6600_v0.9.1.rom',
            },

        ],
        'command': vp24_vp66_command,

    },
    'vp6670': {
        'cpu': '1255U',
        'bios': [
            {
                'vendor': 'ami',
                'file': 'vp6670_ADZ6L714.bin',
            },
            {
                'vendor': 'coreboot',
                'file': 'protectli_vp6600_v0.9.1.rom',
            },

        ],
        'command': vp24_vp66_command,

    },
})
