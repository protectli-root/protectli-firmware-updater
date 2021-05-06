# BIOS Flash

The ```flashbios``` application will detect Protectli-brand host hardware and flash available BIOS images to the BIOS chip. This tool is useful for swapping between AMI and coreboot BIOS, as well as recovering from a bad BIOS configuration.

## Prerequisites

The flash tool requires the following:

1. Protectli Hardware as the machine running the script.
1. A Linux-based operating system (use Ubuntu Live USB if you are unsure)
1. Python3

## Quick Install and Run

Simply clone this repo and run flashbios. Or, check out a release and download it directly.

To clone and run:

```
git clone https://github.com/protectli/flashli.git
cd flashli
./flashbios
```

To obtain a binary, visit the Releases page and select the download you want. The downloaded ZIP (or otherwise compressed file) should be extracted to the host machine however you please (such as by USB thumbdrive). Extract the contents and run ```./flashbios``` from the CLI.

## Developers

To create distributable packages, simply run ```make```. ```make clean``` is also supported for between builds.

### Makefile

```make``` will simply bundle the required resources into a .tar.gz for easy distribution.
