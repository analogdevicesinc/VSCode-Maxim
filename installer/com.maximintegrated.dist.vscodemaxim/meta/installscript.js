function Component()
{
    installer.finishButtonClicked.connect(this, Component.prototype.installationFinished);
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    // // Get System info
    var kernel = systemInfo.kernelType;
    var kernel_version = systemInfo.kernelVersion;
    var arch = systemInfo.currentCpuArchitecture;

    // Create symbolic links for OpenOCD config files to resolve case sensitivity issues on Linux.
    if (kernel == "linux") {
        var target_dir = "@TargetDir@/Tools/OpenOCD/scripts/target";

        // TODO:  Figure out how to import/call QT classes so that I can script this instead of hard-coding
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32520.cfg", target_dir + "/MAX32520.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32650.cfg", target_dir + "/MAX32650.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32655.cfg", target_dir + "/MAX32655.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32660.cfg", target_dir + "/MAX32660.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32665.cfg", target_dir + "/MAX32665.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32665_nsrst.cfg", target_dir + "/MAX32665_nsrst.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32670.cfg", target_dir + "/MAX32670.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32672.cfg", target_dir + "/MAX32672.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32675.cfg", target_dir + "/MAX32675.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32680.cfg", target_dir + "/MAX32680.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max32690.cfg", target_dir + "/MAX32690.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max78000.cfg", target_dir + "/MAX78000.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max78000_nsrst.cfg", target_dir + "/MAX78000_nsrst.cfg");
        component.addOperation("Execute", "ln", "-sf", target_dir + "/max78002.cfg", target_dir + "/MAX78002.cfg");
    }
}

Component.prototype.installationFinished = function() 
{
    // Open readme file to complete installation.
    if (installer.status == QInstaller.Success) {
        var result = QMessageBox.question("vscode-maxim.finished", "Installer", "You have installed Visual Studio Code support for the SDK (VSCode-Maxim).  Some minor manual setup is required to complete the installation, including downloading and installing Visual Studio Code itself.\n\nThe VSCode-Maxim readme will now be opened.  Please follow the installation instructions in that document.\n\nIf you select 'Cancel', the readme will not be opened.  Please complete the installation instructions at a later time.  The readme can be found in the VSCode-Maxim folder inside of the 'Tools' directory in the SDK.", QMessageBox.Ok | QMessageBox.Cancel);

        if (result == QMessageBox.Ok) {
            try {
                QDesktopServices.openUrl("file:///" + installer.value("TargetDir") + "/Tools/VSCode-Maxim/readme.md");
            } catch(e) {
                console.log(e);
                QMessageBox.warning("vscode-maxim.readmefail", "Installer", "Failed to automatically open @TargetDir@/Tools/VSCode-Maxim/readme.md\n\nPlease open this file manually.", QMessageBox.Ok);
            }
        }
    }
}