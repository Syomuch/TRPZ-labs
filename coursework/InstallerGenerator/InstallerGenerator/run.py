import tkinter as tk
from core.gui_creator.gui import InstallerCreatorGUI


if __name__ == '__main__':
    root = tk.Tk()
    app = InstallerCreatorGUI(root)
    root.mainloop()