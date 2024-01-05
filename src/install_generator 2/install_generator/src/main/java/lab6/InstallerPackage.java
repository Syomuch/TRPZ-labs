package lab6;

public interface InstallerPackage {
    void addFile(String file);
    void createDesktopShortcut(boolean create);
    void setLicenseKey(String key);
    void install();
}
