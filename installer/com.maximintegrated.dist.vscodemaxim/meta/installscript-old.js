function Component()
{
    
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    component.addOperation("EnvironmentVariable", "MAXIM_PATH", "@TargetDir@", true, false); // Add MAXIM_PATH to user environment variables.  persistent = true, system = false

    // Get System info
    var kernel = systemInfo.kernelType;
    var kernel_version = systemInfo.kernelVersion;
    var arch = systemInfo.currentCpuArchitecture;

    // Retrieve VS Code installer binaries (https://code.visualstudio.com/docs/supporting/faq#_previous-release-versions)
    var vscode_version = "1.65.2"

    var url = "https://update.code.visualstudio.com/" + vscode_version + "/";
    if (kernel == "winnt") {
        // Windows
        url = url + "win32-"

        if (arch == "x86_64") {
            // Windows 64-bit
            url = url + "x64-user"
        }

    } else if (kernel == "linux") {
        // Linux
        url = url + "linux-"

        if (arch == "x86_64") {
            // Linux 64 bit
            url = url + "x64"
        }

    } else if (kernel == "darwin") {
        // MacOS
        url = url + "darwin"  
    }

    url = url + "/stable"

    // Is it OK to retrieve VS Code?
    var retrieve = false;
    var res = QMessageBox.question("vscode.question", "Installer", "This installer will now download and install Visual Studio Code from the following URL: \n" + url + "\nIs this OK?\nIf you select 'No', please download and install Visual Studio Code manually.", QMessageBox.Yes | QMessageBox.No);
    if (res == QMessageBox.Yes) { retrieve = true; }

    if (retrieve && kernel == "winnt") {
        // Download installer with Invoke-WebRequest and run it
        // Need to run in the same command because the download file doesn't get created on time if download and run are separated.
        component.addOperation("Execute", "powershell", "$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest \"" + url + "\" -o vscode-installer.exe; Start-Process vscode-installer.exe -Wait; rm vscode-installer.exe");
        // $ProgressPreference = 'SilentlyContinue' disables the powershell progress bar.  The progress bar slows down the download

    } else if (retrieve && (kernel == "linux" || kernel == "darwin")) {
        // Download installer with wget
        component.addOperation("Execute", "wget", "\"" + url + "\" -o vscode-installer & vscode-installer & rm vscode-installer");
    }
}