package lab6;

import lab4and5.InstallerPackage;

public class WindowsInstallerPackage extends InstallerPackage {
    // Реалізація методів інтерфейсу для Windows

    public WindowsInstallerPackage() {
        super();
    }

    @Override
    public void addFile(String file) {
        // Логіка додавання файлу для Windows
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

    // Інші методи для конфігурації пакету для Windows

    @Override
    public void install() {
        // Логіка інсталяції для Windows
        super.install();
    }
}
