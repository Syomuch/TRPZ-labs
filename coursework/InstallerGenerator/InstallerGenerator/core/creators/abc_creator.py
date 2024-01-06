from abc import ABC, abstractmethod


class InstallerCreator(ABC):
    """
    An abstract base class for creating installers.

    Attributes:
        source_directory (str): Source directory of files to include in the installer.
        output_directory (str): Output directory for the generated installer.
        file_list (list): List of files to include in the installer.
        installer_name (str): Name of the installer to be created.
    """

    def __init__(self, source_directory, output_directory, file_list, installer_name):
        """
        Initializes the InstallerCreator with necessary information.

        Args:
            source_directory (str): Source directory of files.
            output_directory (str): Output directory for the installer.
            file_list (list): List of files to include.
            installer_name (str): Name of the installer.
        """
        self.source_directory = source_directory
        self.output_directory = output_directory
        self.file_list = file_list
        self.installer_name = installer_name

    @abstractmethod
    def create_installer(self):
        """
        Abstract method to create an installer.

        This method must be implemented by subclasses.
        """
        pass