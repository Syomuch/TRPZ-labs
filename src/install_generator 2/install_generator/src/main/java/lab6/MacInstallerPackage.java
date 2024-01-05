package lab6;

import lab4and5.InstallerPackage;

public class MacInstallerPackage extends InstallerPackage {
    // Реалізація методів інтерфейсу для Mac

    public MacInstallerPackage() {
        super();
    }

    @Override
    public void addFile(String file) {
        super.addFile(file);
    }

    @Override
    public void createDesktopShortcut(boolean create) {
        super.createDesktopShortcut(create);
    }

    @Override
    public void setLicenseKey(String key) {
        super.setLicenseKey(key);
    }

    // Інші методи для конфігурації пакету для Mac

    @Override
    public void install() {
        super.install();
    }
}
