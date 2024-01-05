package lab6;

public class InstallerPackageFactory {
    public static InstallerPackage createInstallerPackage(String platform) {
        if (platform.equalsIgnoreCase("Windows")) {
            return new WindowsInstallerPackage();
        } else if (platform.equalsIgnoreCase("Mac")) {
            return new MacInstallerPackage();
        } else {
            throw new IllegalArgumentException("Unsupported platform");
        }
    }
}
