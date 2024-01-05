package lab7;

import lab6.InstallerPackage;
import lab6.InstallerPackageFactory;

// Приклад розділення інсталяційних реалізацій для різних платформ( патерн міст)
public class WindowsInstallerPlatform implements InstallerPlatform {
    @Override
    public void performInstall() {
        InstallerPackage windowsPackage = InstallerPackageFactory.createInstallerPackage("Windows");
        windowsPackage.addFile("file1.exe");
        windowsPackage.addFile("file2.dll");
        windowsPackage.createDesktopShortcut(true);
        windowsPackage.setLicenseKey("abc123");
        windowsPackage.install();
    }
}
