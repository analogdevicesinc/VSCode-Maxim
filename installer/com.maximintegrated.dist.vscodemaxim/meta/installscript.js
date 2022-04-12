function Component()
{
    
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    // // Get System info
    var kernel = systemInfo.kernelType;
    var kernel_version = systemInfo.kernelVersion;
    var arch = systemInfo.currentCpuArchitecture;

    // Symbolic links for OpenOCD config files should be created in
    // the target package's installscript.js to resolve case sensitivity
    // on Linux

    if (component.enabled) {
        installer.finishButtonClicked.connect(this, Component.prototype.installationFinished);
    }
}

Component.prototype.installationFinished = function() 
{
    var tag = "v1.4.0";
    var tag_url = "https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/tree/" + tag;
    var release_url = "https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases/tag/" + tag;
    
    // Open readme file to complete installation.
    // isInstaller() = true on fresh install
    // isPackageManager() = true on "Add/remove components"
    // https://doc.qt.io/qtinstallerframework/scripting-installer.html
    if ((installer.isInstaller() || installer.isPackageManager()) && installer.status == QInstaller.Success) {
        var result = QMessageBox.question("vscode-maxim.finished", "MaximSDK Installer", "You have installed Visual Studio Code support for the SDK (VSCode-Maxim).  Some minor manual setup is required to complete the installation.\n\nThe VSCode-Maxim readme will now be opened in your browser.  Please follow the installation instructions in that document.\n\nIf you select 'Cancel', the readme will not be opened.  Please complete the installation instructions at a later time.  The readme can be found in the VSCode-Maxim folder inside of the 'Tools' directory in the SDK.", QMessageBox.Ok | QMessageBox.Cancel);

        if (result == QMessageBox.Ok) {
            try {
                QDesktopServices.openUrl(tag_url + "/readme.md#vscode-maxim");
            } catch(e) {
                console.log(e);
                QMessageBox.warning("vscode-maxim.readmefail", "MaximSDK Installer", "Failed to open the online copy of the readme.\n\nPlease open this file manually (@TargetDir@/Tools/VSCode-Maxim/readme.md)", QMessageBox.Ok);
            }
        }
    } 
    
    // Open release notes on update.
    // isUpdater() = true in update mode
    else if (installer.isUpdater() && installer.status == QInstaller.Success) {
        var result = QMessageBox.question("vscode-maxim.finished", "MaximSDK Installer", "Visual Studio Code support for the Maxim Microcontrollers SDK (VSCode-Maxim) has been updated to" + tag + "\n\nThe release notes for this update will now be opened in your browser.", QMessageBox.Ok | QMessageBox.Cancel);

        if (result == QMessageBox.Ok) {
            try {
                QDesktopServices.openUrl(release_url);
            } catch(e) {
                console.log(e);
                QMessageBox.warning("vscode-maxim.releasefail", "MaximSDK Installer", "Failed to open the online release notes.",QMessageBox.Ok);
            }
        }
    }
}