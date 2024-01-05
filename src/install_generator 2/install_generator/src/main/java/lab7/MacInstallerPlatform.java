package lab7;

import lab6.InstallerPackage;
import lab6.InstallerPackageFactory;

// Приклад розділення інсталяційних реалізацій для різних платформ( патерн міст)
public class MacInstallerPlatform implements InstallerPlatform{
    @Override
    public void performInstall() {
        InstallerPackage macPackage = InstallerPackageFactory.createInstallerPackage("Mac");
        macPackage.addFile("file1.app");
        macPackage.addFile("file2.dylib");
        macPackage.createDesktopShortcut(true);
        macPackage.setLicenseKey("def456");
        macPackage.install();
    }
}
