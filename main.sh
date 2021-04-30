#!/bin/sh

[ $(id -u) -ne 0 ] && echo "You must be root." && exit 1

cd /tmp
rm -rf bios-flash-master/
rm -rf bios-flash-master.zip
wget -q https://gitlab.protectli.com/protectli/bios-flash/-/archive/master/bios-flash-master.zip
unzip -q bios-flash-master.zip
echo "BIOS Flash is ready. Run the following command as root to execute BIOS Flash:"
echo "  /tmp/bios-flash-master/main.py"
exit 0
