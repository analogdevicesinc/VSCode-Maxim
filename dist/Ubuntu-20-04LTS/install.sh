# MaximSDK installer with VS Code support.  Run sudo as user, ex: sudo -u [your username] bash install.sh

echo "Updating package lists..."
sudo apt update

read -p "Install the MaximSDK?  (y/n)" YN
if [ "$YN" = "y" ] || [ "$YN" = "Y" ]; then
	echo
	echo "Installing MaximSDK..."
	wget http://www.mxim.net/product/msdk/MaximMicrosSDK_linux.run
	chmod +x ./MaximMicrosSDK_linux.run
	./MaximMicrosSDK_linux.run

	echo "Checking any missing packages..."
	sudo apt install --yes make libncurses5 libusb-1.0-0 libusb-0.1-4 libhidapi-libusb0 libhidapi-hidraw0

	echo "Copying OpenOCD rules file..."
	sudo cp 60-openocd.rules /etc/udev/rules.d/
	echo "Refreshing udev..."
	sudo udevadm control --reload && udevadm trigger

	echo "Cleaning up..."
	rm ./MaximMicrosSDK_linux.run

	echo "Done!"

fi
echo
echo "Installing Visual Studio Code..."
sudo apt install code
code --install-extension ms-vscode.cpptools

echo "Done!  VS Code and required extensions are installed."
echo "Additional setup is still required."
echo "Run setup.sh (Ex: bash setup.sh) or see https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#linux for more detailed instructions on completing the installation."
