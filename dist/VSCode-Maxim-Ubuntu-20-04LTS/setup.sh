# VSCode-Maxim setup script.  **Run as user**, ex:  sudo -u [username] bash setup.sh

if [ ! -f ./MaintenanceTool.dat ]; then
	# Running script outside of MaximSDK
	echo "This script is not located inside the root directory of a MaximSDK installation..."
	
	if [ -z "$MAXIM_PATH" ]; then
		# No environment variable.  Collect path manually?
		echo "Failed to locate MAXIM_PATH environment variable..."
		echo "Please set MAXIM_PATH or place this script in the root directory of the MaximSDK installation and try again."
		read -p "Alternatively, enter the MaximSDK installation path manually now? (y/n):" YN
		if [ "$YN" = "y" ] || [ "$YN" = "Y" ]; then
			read -p "Enter the full path of the MaximSDK installation (ex: /home/username/MaximSDK):" MAXIM_PATH
			echo "Verifying..."
		else
			echo "Quitting..."
			exit -1
		fi
	else
		# Verify current environment variable is correct
		echo "Located $MAXIM_PATH"
		read -p "Is this the correct location of the latest MaximSDK installation? (y/n):" YN
		if [ "$YN" = "y" ] || [ "$YN" = "Y" ]; then
			echo "Verifying..."
		elif [ "$YN" = "n" ] || [ "$YN" = "N" ]; then	
			read -p "Enter the full path of the MaximSDK installation (ex: /home/username/MaximSDK):" MAXIM_PATH
			echo "Verifying..."
		else
			exit -1
		fi
	fi
else
	# Running from inside MaximSDK.  Set MAXIM_PATH to location of this script
	BASEDIR=$(dirname $0)
	MAXIM_PATH="$(cd $BASEDIR && pwd)"
fi

# Final verify
if [ ! -f $MAXIM_PATH/MaintenanceTool.dat ]; then
	echo "Verification of MaximSDK installation failed.  Failed to find expected files."
	exit -2
else
	echo "Verified SDK location!"
fi

#Get user's home directory
HOME_DIR=$(getent passwd ${SUDO_USER:-$USER} | cut -d: -f6) # This should work if this script is run with sudo or normally
echo "Located user home directory at $HOME_DIR..."

# Add MAXIM_PATH to environment variables
echo "Adding MAXIM_PATH environment variable..."
if [ -f $HOME_DIR/.bashrc ]; then

	# .bashrc setup

	echo "Detected $HOME_DIR/.bashrc..."
	if [ -z "$(grep "export MAXIM_PATH=" $HOME_DIR/.bashrc)" ]; then
		# If grep search for MAXIM_PATH in ~/.bashrc returns empty string (-z)
		echo "Setting MAXIM_PATH=$MAXIM_PATH in $HOME_DIR/.bashrc"
		sed -i~ "1iexport MAXIM_PATH=${MAXIM_PATH}" $HOME_DIR/.bashrc # Insert line at beginning (1i) and create backup (-i~)
	else
		# Update MAXIM_PATH instead of adding new line
		echo "$HOME_DIR/.bashrc already sets MAXIM_PATH.  Updating to MAXIM_PATH=$MAXIM_PATH just in case"
		sed -i~ "s:.*export MAXIM_PATH=.*:export MAXIM_PATH=$MAXIM_PATH:" $HOME_DIR/.bashrc
	fi

	echo "Reloading shell..."
	source $HOME_DIR/.bashrc
fi

# Get newer GCC
GCC_VERSION="10.3.1"
GCC_PATH="$MAXIM_PATH/Tools/GNUTools/gcc-arm-none-eabi-$GCC_VERSION"
ARM_LINK="https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2"
PACKAGE_NAME="gcc-arm-none-eabi-10.3-2021.10"
echo "Getting Arm embedded toolchain v$GCC_VERSION..."
if [ ! -d $GCC_PATH ]; then
	wget -O gcc-arm.tar.bz2 $ARM_LINK
	mkdir -p $GCC_PATH
	tar -xvf gcc-arm.tar.bz2 --directory $MAXIM_PATH/Tools/GNUTools/
	cp -rf $MAXIM_PATH/Tools/GNUTools/$PACKAGE_NAME/* $GCC_PATH/
	echo "Cleaning up..."
	rm -rf $MAXIM_PATH/Tools/GNUTools/$PACKAGE_NAME
	rm gcc-arm.tar.bz2
else
	echo "Already have $GCC_PATH"
fi

# Generate VS Code project files
echo "Generating VS Code project files..."
./generate SDK

echo "Done!"
