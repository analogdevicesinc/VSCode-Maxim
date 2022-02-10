# VSCode-Maxim setup script.  **Run as user with non-elevated privileges**, ex:  bash setup.sh

SCRIPTDIR=$(cd $(dirname $0) && pwd)
echo "Running setup.sh from $SCRIPTDIR"

ENV_FILE=/etc/profile.d/maximsdk-env.sh

# Check for existence of environment variable shell script on startup so we can refresh if needed
if [ -f $ENV_FILE ]; then
	source $ENV_FILE
else
	echo "Failed to find /etc/profile.d/maximsdk-env.sh"
fi

VERIFICATION_DIR=Libraries/CMSIS/Device/Maxim
if [ ! -d ./$VERIFICATION_DIR ]; then
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
			read -p "Enter the full path of the latest MaximSDK installation (ex: /home/username/MaximSDK):" MAXIM_PATH
			echo "Verifying..."
		else
			exit -1
		fi
	fi
else
	# Running from inside MaximSDK.  Set MAXIM_PATH to location of this script
	MAXIM_PATH=$SCRIPTDIR
fi

# Final verify
if [ ! -d $MAXIM_PATH/$VERIFICATION_DIR ]; then
	echo "Verification of MaximSDK installation failed.  Failed to find expected files."
	exit -2
else
	echo "Verified SDK location!"
fi

# Add MAXIM_PATH to system environment variables
echo "Adding MAXIM_PATH environment variable..."
if [ -f $ENV_FILE ]; then
	# Update existing file
	echo "Updating $ENV_FILE ..."
	if [ -z "$(sudo grep "export MAXIM_PATH=" $ENV_FILE)" ]; then
		# If grep search for MAXIM_PATH returns empty string (-z)
		echo "Setting MAXIM_PATH=$MAXIM_PATH"
		sudo sed -i~ "1iexport MAXIM_PATH=${MAXIM_PATH}" $ENV_FILE # Insert line at beginning (1i) and create backup (-i~)
	else
		# Update MAXIM_PATH instead of adding new line
		echo "$ENV_FILE already sets MAXIM_PATH.  Updating to use MAXIM_PATH=$MAXIM_PATH"
		sudo sed -i~ "s:.*export MAXIM_PATH=.*:export MAXIM_PATH=$MAXIM_PATH:" $ENV_FILE # search and replace (s):pattern (.*=all):with this:
	fi

	echo "Reloading shell..."
	source $ENV_FILE
else
	# Create new file
	sudo touch $ENV_FILE
	sudo sed -i "1iexport MAXIM_PATH=${MAXIM_PATH}" $ENV_FILE
fi

# Run updates.sh
if [ -f $MAXIM_PATH/updates.sh ]; then
	echo "Checking for updates..."
	cd $MAXIM_PATH && bash updates.sh
	cd $SCRIPTDIR
fi


# Get newer GCC
GCC_VERSION="10.3.1"
ARCH=$(arch)
PACKAGE_STRING="10.3-2021.10"
GCC_PATH="$MAXIM_PATH/Tools/GNUTools/gcc-arm-none-eabi-$GCC_VERSION"
ARM_LINK="https://developer.arm.com/-/media/Files/downloads/gnu-rm/$PACKAGE_STRING/gcc-arm-none-eabi-$PACKAGE_STRING-$ARCH-linux.tar.bz2"

echo "Getting Arm embedded toolchain v$GCC_VERSION"
if [ ! -d $GCC_PATH ]; then
	wget -O gcc-arm.tar.bz2 $ARM_LINK
	mkdir -p $GCC_PATH
	tar -xvf gcc-arm.tar.bz2
	cp -rf gcc-arm-none-eabi-$PACKAGE_STRING/* $GCC_PATH/
	echo "Cleaning up..."
	rm -rf gcc-arm-none-eabi-$PACKAGE_STRING
	rm gcc-arm.tar.bz2
else
	echo "Already have $GCC_PATH"
fi

# Generate VS Code project files
echo "Generating VS Code project files..."
./generate SDK

echo "Done!"
