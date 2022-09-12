#!/bin/bash
# Check if the user is root.
# If it's not, run the installation as root.
if [[ $EUID -ne 0 ]]; then
    echo "\033[0;31mThe installation must be run as root."
    echo "\033[0;31mPlease enter your password:\033[0m"
    sudo "$0" "curl https://raw.githubusercontent.com/Kapsulon/kepm/main/install_script.sh | sudo sh"
    exit $?
fi

# ------- START CLEANING -------
# Remove temporary files
if [ -d "/tmp/kepm" ]; then
    rm -rf /tmp/kepm
fi

if [ -d "/usr/local/lib/kepm" ]; then
    rm -r /usr/local/lib/kepm
fi

if [ $? -ne 0 ]; then
    tput setaf 1
    echo "=> Unable to clean temporary files."
    tput init
    tput setab 1
    echo "=> Installation failed."
    tput init
    exit 1
fi

tput setaf 2
echo "=> Removed temporary files."
tput init
echo ""
# -------- END CLEANING -------

#  ------ START INSTALLATION -----
cd /tmp
tput setaf 6
echo "=> Cloning KEPM source code..."
tput init
echo ""
git clone https://github.com/Kapsulon/kepm.git
pip install -r kepm/requirements.txt --user
pip3 install -r kepm/requirements.txt --user
echo ""
if [ $? -ne 0 ]; then
    tput setaf 1
    echo "=> Unable to clone KEPM source code."
    tput init
    tput setab 1
    echo "=> Installation failed."
    tput init
    exit 1
fi
tput setaf 2
echo "=> Cloned KEPM source code."
echo ""
tput setaf 6
echo "=> Copying source files..."
tput init
sudo cp -R kepm /usr/local/lib/kepm
sudo cp /usr/local/lib/kepm/kepm /usr/local/bin/kepm
tput setaf 2
echo "=> Copied source files."
tput init
# ------- END INSTALLATION -------

# ------ GIVING PERMS --------
echo ""
tput setaf 6
echo "=> Giving run permissions..."
tput init
sudo chmod -R 777 /usr/local/lib/kepm
sudo chmod 777 /usr/local/bin/kepm
if [ $? -ne 0 ]; then
    tput setaf 1
    echo "=> Unable to give run permissions."
    tput init
    tput setab 1
    echo "=> Installation failed."
    tput init
    exit 1
fi
tput init
tput setaf 2
echo "=> Permissions OK."
tput init
# ----- END GIVING PERMS -----

# ------ START INSTALL CLEAN -----
echo ""
tput setaf 6
echo "=> Cleaning installation..."
tput init
sudo rm -rf /tmp/kepm
sudo rm -f /usr/local/lib/kepm/kepm
if [ $? -ne 0 ]; then
    tput setaf 1
    echo "=> Unable to clean installation."
    tput init
    tput setab 1
    echo "=> Installation failed."
    tput init
    exit 1
fi
tput init
tput setaf 2
echo "=> Installation cleaned."
tput init
tput setab 2
tput blink
echo "=> Installation complete."
tput init
exit 0
# ------ END INSTALL CLEAN ------
