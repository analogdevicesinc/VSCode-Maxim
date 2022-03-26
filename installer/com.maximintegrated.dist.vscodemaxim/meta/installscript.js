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

    // TODO: Set MAXIM_PATH on Linux and MacOS
}