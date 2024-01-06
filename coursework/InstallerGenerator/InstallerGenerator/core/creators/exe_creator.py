import os
import subprocess
from typing import List, Iterator

from .abc_creator import InstallerCreator
from ..base_config import inno_setup_compiler
from ..iterator import FileListIterator
from ..factories.installer_flyweight import InstallerFlyweightFactory

class EXECreator(InstallerCreator):
    """
    Class for creating an EXE installer.

    Attributes:
        source_directory (str): Directory where source files are located.
        output_directory (str): Directory where the EXE installer will be created.
        file_list (List[str]): List of files to be included in the installer.
        installer_name (str): Name of the installer.
    """

    def __init__(self, source_directory: str, output_directory: str, file_list: List[str], installer_name: str):
        """
        Initialize the EXECreator.

        Args:
            source_directory (str): Directory containing the source files.
            output_directory (str): Output directory for the installer.
            file_list (List[str]): List of files to include in the installer.
            installer_name (str): Name for the EXE file.
        """
        self.source_directory: str = source_directory
        self.output_directory: str = output_directory
        self.file_list: List[str] = file_list
        self.installer_name: str = installer_name

    def __iter__(self) -> Iterator[str]:
        """
        Returns an iterator for the file list.

        Returns:
            FileListIterator: An iterator for the file list.
        """
        return FileListIterator(self.file_list)

    def create_installer(self) -> None:
        """
        Creates an EXE installer.

        This method handles the logic for generating an EXE installer.
        """
        if not self.file_list:
            print("No files selected. Please select files to include in the installer.")
            return

        if not self.installer_name:
            print("Please enter a name for the EXE file.")
            return

        script_path = os.path.join(self.output_directory, "setup_script.iss")
        with open(script_path, "w") as script_file:
            script_file.write(self.generate_inno_setup_script())

        inno_setup_compiler = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        compile_command = [inno_setup_compiler, script_path]

        flyweight = InstallerFlyweightFactory.get_flyweight("EXE")
        flyweight.compile_script(compile_command)

        print("EXE installer created successfully in the output directory.")

    def generate_inno_setup_script(self) -> str:
        """
        Generates an Inno Setup script for the installer.

        Returns:
            str: A string containing the Inno Setup script.
        """
        script = f"""
                    [Setup]
                    AppName={self.installer_name}
                    AppVersion=1.0
                    DefaultDirName={{autopf}}\\{self.installer_name}
                    OutputDir={self.output_directory}
                    OutputBaseFilename={self.installer_name}_installer
                    Compression=lzma
                    SolidCompression=yes
                    [Files]
                    """

        for file in self:
            script += f"Source: \"{os.path.join(self.source_directory, file)}\"; DestDir: \"{{app}}\"\n"
        return script

    def compile_exe_script(self, script_path: str) -> None:
        """
        Compiles the EXE script using Inno Setup Compiler.

        Args:
            script_path (str): Path to the script file.
        """

        compile_command = [inno_setup_compiler, script_path]
        compile_result = subprocess.run(compile_command, capture_output=True, text=True)
        if compile_result.returncode != 0:
            print(f"Inno Setup error output: {compile_result.stderr}")
            return
        print(f"Inno Setup output: {compile_result.stdout}")
        print("EXE installer created successfully in the output directory.")
