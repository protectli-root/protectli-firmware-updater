# BIOS Flash

    -Ensure you are connected to the local network and have internet access
    -Use wget to obtain the zip file 

        wget https://gitlab.protectli.com/protectli/bios-flash/-/archive/master/bios-flash-master.zip

    -Make sure the zip file is in your working directory "bios-flash-master.zip"

        ls -la

    -Unzip the "bios-flash-master.zip"

        unzip bios-flash-master.zip

    -Verify that the zip file has unzipped and there is a "bios-flash-master" folder

        ls -la

    -Change into the "bios-flash-master" directory

        cd bios-flash-master

    -Verify you are in the bios-flash-master folder

        ls -la

    -Run the script

        sudo python3 main.py

    -After the script has started to run, you will be prompted to enter a password.
    -Use the password for ubuntu user account
