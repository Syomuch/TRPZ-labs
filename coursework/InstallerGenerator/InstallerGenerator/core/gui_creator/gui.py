import os
import tkinter as tk
from tkinter import filedialog, ttk
import winshell
from ..creators.exe_creator import EXECreator
from ..creators.msi_creator import MSICreator
from ..proxy import InstallerCreatorProxy
class InstallerCreatorGUI:
    """
    Graphical User Interface for creating installers.

    This class provides a user-friendly interface for configuring and generating MSI and EXE installers.
    """
    def __init__(self, root):
        """
        Initialize the InstallerCreatorGUI instance.

        Args:
            root (tk.Tk): The root window of the GUI.
        """
        self.root = root
        self.create_msi = tk.BooleanVar()
        self.create_exe = tk.BooleanVar()
        self.create_shortcut = tk.BooleanVar()
        self.source_directory = tk.StringVar()
        self.selected_output_directory = tk.StringVar()
        self.installer_filename = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components.

        This method calls various setup methods to configure the GUI's styles, layout, controls, and actions.
        """
        self.setup_styles()
        self.setup_layout()
        self.setup_directory_controls()
        self.setup_file_list()
        self.setup_output_controls()
        self.setup_installer_controls()
        self.setup_action_controls()

    def setup_styles(self):
        """
        Set up styles for GUI elements.

        This method configures styles for background color, foreground color, and focus color.
        """
        self.style_args = {'bg': 'black', 'fg': 'white'}
        self.entry_style_args = {'bg': '#1a1a1a', 'fg': 'white', 'insertbackground': 'white'}
        self.listbox_style_args = {'bg': '#1a1a1a', 'fg': 'white'}
        self.button_style_args = {'bg': '#333333', 'fg': 'white', 'activebackground': '#4d4d4d', 'activeforeground': 'white'}

        style = ttk.Style()
        style.configure("TCheckbutton", background='black', foreground='white', focuscolor=style.configure(".")["background"])

    def setup_layout(self):
        """
        Set up the GUI layout.

        This method creates a left frame with a black background.
        """
        self.left_frame = tk.Frame(self.root, bg='black')
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    def setup_directory_controls(self):
        """
        Set up controls for selecting the source directory.

        This method includes a label, an entry field for the directory path, and a browse button.
        """
        directory_label = tk.Label(self.left_frame, text="Select source directory for files:", **self.style_args)
        directory_label.pack(anchor='w', pady=(5, 0))

        self.directory_entry = tk.Entry(self.left_frame, textvariable=self.source_directory, **self.entry_style_args)
        self.directory_entry.pack(fill='x', padx=5, pady=5)

        browse_directory_button = tk.Button(self.left_frame, text="Browse", command=self.browse_directory, **self.button_style_args)
        browse_directory_button.pack(anchor='w', padx=5)

    def setup_file_list(self):
        """
        Set up the file list control.

        This method creates a Listbox with multiple selection mode for selecting files to include in the installer.
        """
        file_list_label = tk.Label(self.left_frame, text="Select files to include:", **self.style_args)
        file_list_label.pack(anchor='w', pady=(5, 0))

        self.file_listbox = tk.Listbox(self.left_frame, selectmode=tk.MULTIPLE, **self.listbox_style_args)
        self.file_listbox.pack(fill='both', expand=True, padx=5, pady=5)

    def setup_output_controls(self):
        """
        Set up controls for selecting the output directory.

        This method includes a label, an entry field for the directory path, and a browse button.
        """
        output_directory_label = tk.Label(self.left_frame, text="Select output directory for the installer:", **self.style_args)
        output_directory_label.pack(anchor='w', pady=(5, 0))

        self.output_directory_entry = tk.Entry(self.left_frame, textvariable=self.selected_output_directory, **self.entry_style_args)
        self.output_directory_entry.pack(fill='x', padx=5, pady=5)

        browse_output_button = tk.Button(self.left_frame, text="Browse", command=self.browse_output_directory, **self.button_style_args)
        browse_output_button.pack(anchor='w', padx=5)

    def setup_installer_controls(self):
        """
        Set up controls for configuring the installer.

        This method includes input fields for the installer name and checkboxes for various installer options.
        """
        installer_filename_label = tk.Label(self.left_frame, text="Installer file name:", **self.style_args)
        installer_filename_label.pack(anchor='w', pady=(5, 0))

        self.installer_filename_entry = tk.Entry(self.left_frame, textvariable=self.installer_filename, **self.entry_style_args)
        self.installer_filename_entry.pack(fill='x', padx=5, pady=5)

        shortcut_checkbox = ttk.Checkbutton(self.left_frame, text="Create Desktop Shortcut", style="TCheckbutton", variable=self.create_shortcut)
        shortcut_checkbox.pack(anchor='w', padx=5, pady=(0, 5))

        msi_checkbox = ttk.Checkbutton(self.left_frame, text="Create MSI", style="TCheckbutton", variable=self.create_msi)
        msi_checkbox.pack(anchor='w', padx=5, pady=(0, 5))

        exe_checkbox = ttk.Checkbutton(self.left_frame, text="Create EXE", style="TCheckbutton", variable=self.create_exe)
        exe_checkbox.pack(anchor='w', padx=5, pady=(0, 5))

    def setup_action_controls(self):
        """
        Set up controls for actions like creating the installer.

        This method includes a button to create the installer and a label for displaying the result.
        """
        create_installer_button = tk.Button(self.left_frame, text="Create Installer", command=self.create_installer, **self.button_style_args)
        create_installer_button.pack(anchor='w', padx=5, pady=5)

        self.result_label = tk.Label(self.left_frame, text="", **self.style_args)
        self.result_label.pack(anchor='w', pady=(5, 0))

    def browse_directory(self):
        """
        Open a directory dialog to select the source directory.

        Updates the source directory entry field and updates the file list.
        """
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.source_directory.set(directory_path)
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory_path)
            self.update_file_list(directory_path)

    def update_file_list(self, directory_path):
        """
        Update the file list based on the selected source directory.

        Args:
            directory_path (str): The path of the selected source directory.
        """
        self.file_listbox.delete(0, tk.END)
        for filename in os.listdir(directory_path):
            self.file_listbox.insert(tk.END, filename)

    def browse_output_directory(self):
        """
        Open a directory dialog to select the output directory for the installer.

        Updates the output directory entry field.
        """
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.selected_output_directory.set(directory_path)
            self.output_directory_entry.delete(0, tk.END)
            self.output_directory_entry.insert(0, directory_path)

    def create_installer_factory(self, installer_type, source_directory, output_directory, file_list, installer_name):
        """
        Create an installer factory for MSI or EXE.

        Args:
            installer_type (str): The type of installer to create (MSI or EXE).
            source_directory (str): The source directory of files.
            output_directory (str): The output directory for the installer.
            file_list (list): List of files to include in the installer.
            installer_name (str): Name of the installer.

        Returns:
            InstallerCreatorProxy: An instance of an installer creator factory.
        """
        if installer_type == 'MSI':
            real_creator = MSICreator(source_directory, output_directory, file_list, installer_name)
        elif installer_type == 'EXE':
            real_creator = EXECreator(source_directory, output_directory, file_list, installer_name)
        else:
            raise ValueError("Unknown installer type")

        return InstallerCreatorProxy(real_creator, installer_type)

    def create_installer(self):
        """
        Create the installer based on user inputs.

        Calls the appropriate installer creator based on selected checkboxes (MSI or EXE).
        Creates a desktop shortcut if the corresponding checkbox is selected.
        Displays the result in the GUI.
        """
        installer_name = self.installer_filename.get()
        source_directory = self.source_directory.get()
        output_directory = self.selected_output_directory.get()

        if not installer_name:
            self.result_label.config(text="Please enter a name for the installer.")
            return

        if not source_directory or not output_directory:
            self.result_label.config(text="Please select both source and output directories.")
            return

        file_list = [self.file_listbox.get(idx) for idx in self.file_listbox.curselection()]

        if self.create_msi.get():
            msi_creator = self.create_installer_factory('MSI', source_directory, output_directory, file_list, installer_name)
            msi_creator.create_installer()

        if self.create_exe.get():
            exe_creator = self.create_installer_factory('EXE', source_directory, output_directory, file_list, installer_name)
            exe_creator.create_installer()

        if self.create_shortcut.get():
            self.create_desktop_shortcut(installer_name)

        self.result_label.config(text="Installer creation completed.")

    def create_desktop_shortcut(self, installer_name):
        """
        Create a desktop shortcut for the installer.

        Args:
            installer_name (str): Name of the installer.
        """
        output_directory = self.selected_output_directory.get()

        shortcut_path = os.path.join(winshell.desktop(), installer_name + '.lnk')

        target = os.path.join(output_directory, installer_name + '.exe')

        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = target
            shortcut.description = "Shortcut to " + installer_name
            shortcut.working_directory = output_directory