package lab4and5;

import java.util.List;

public class InstallerIterator implements Iterator {
    private int currentIndex = 0;
    private List<String> files;

    public InstallerIterator(List<String> files) {
        this.files = files;
    }

    @Override
    public boolean hasNext() {
        return currentIndex < files.size();
    }

    @Override
    public Object next() {
        if (hasNext()) {
            return files.get(currentIndex++);
        }
        return null;
    }
}
