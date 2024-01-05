package lab4and5;

import java.util.ArrayList;
import java.util.List;

public class InstallerPackage implements lab6.InstallerPackage {
    private List<String> files;

    public Iterator createIterator() {
        return new InstallerIterator(files);
    }

    private boolean createDesktopShortcut;
    private String licenseKey;

    protected InstallerPackage() {
        this.files = new ArrayList<>();
    }

    // Метод для додавання файлів у пакет
    public void addFile(String file) {
        files.add(file);
    }

    // Метод для встановлення створення ярлика на робочому столі
    public void createDesktopShortcut(boolean create) {
        this.createDesktopShortcut = create;
    }

    // Метод для встановлення ліцензійного ключа
    public void setLicenseKey(String key) {
        this.licenseKey = key;
    }

    @Override
    public void install() {
        // Логіка інсталяції
    }

    // Клас-будівник для створення конфігурацій пакету
    public static class Builder {
        private final InstallerPackage packageToBuild;

        public Builder() {
            packageToBuild = new InstallerPackage();
        }

        // Методи для додавання файлів, настройки ярлика та ліцензійного ключа
        public Builder addFile(String file) {
            packageToBuild.addFile(file);
            return this;
        }

        public Builder createDesktopShortcut(boolean create) {
            packageToBuild.createDesktopShortcut(create);
            return this;
        }

        public Builder setLicenseKey(String key) {
            packageToBuild.setLicenseKey(key);
            return this;
        }

        // Метод для побудови інсталяційного пакету з конфігурацією
        public InstallerPackage build() {
            return packageToBuild;
        }
    }
}
