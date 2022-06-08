# BIOS Flash

The ```flashbios``` application will detect Protectli-brand host hardware and flash available BIOS images to the BIOS chip. This tool is useful for swapping between AMI and coreboot BIOS, as well as recovering from a bad BIOS configuration.

## Prerequisites

The flash tool requires the following:

1. Protectli Hardware as the machine running the script.
1. A Linux-based operating system (use Ubuntu Live USB if you are unsure)
1. Python3

## Quick Install and Run

Download the latest release, uncompress it, and run the flashbios script

```
wget https://github.com/protectli-root/protectli-firmware-updater/releases/download/v1.1.21/flashli.tar.gz
tar -zxvf flashli.tar.gz
cd protectli-firmware-updater-1.1.21/
./flashbios
```

Or clone this repo for the source code and run flashbios. To clone and run:

```
git clone https://github.com/protectli-root/protectli-firmware-updater.git
cd protectli-firmware-updater
./flashbios
```

To obtain a binary, visit the Releases page and select the download you want. The downloaded ZIP (or otherwise compressed file) should be extracted to the host machine however you please (such as by USB thumbdrive). Extract the contents and run ```./flashbios``` from the CLI.

## Developers

To create distributable packages, simply run ```make```. ```make clean``` is also supported for between builds.

### Makefile

```make``` will simply bundle the required resources into a .tar.gz for easy distribution.

### Creating flashrom binary manually

If you wish to build your own flashrom, you can replicate our build with

```
git checkout https://github.com/flashrom/flashrom.git
cd flashrom
make CONFIG_NOTHING=yes CONFIG_INTERNAL=yes CONFIG_DUMMY=yes
```
