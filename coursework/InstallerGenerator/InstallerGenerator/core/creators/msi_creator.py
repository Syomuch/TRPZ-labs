import os
import subprocess
import uuid
from typing import List

from ..base_config import candle_exe_path, light_exe_path
from ..factories.installer_flyweight import InstallerFlyweightFactory
from .abc_creator import InstallerCreator

class MSICreator(InstallerCreator):
    """
    Class for creating an MSI installer.

    Attributes:
        source_directory (str): Directory where source files are located.
        output_directory (str): Directory where the MSI installer will be created.
        file_list (List[str]): List of files to be included in the installer.
        installer_name (str): Name of the installer.
    """
    def __init__(self, source_directory: str, output_directory: str, file_list: List[str], installer_name: str):
        """
        Initialize the MSICreator.

        Args:
            source_directory (str): Directory containing the source files.
            output_directory (str): Output directory for the installer.
            file_list (List[str]): List of files to include in the installer.
            installer_name (str): Name for the MSI file.
        """
        self.source_directory: str = source_directory
        self.output_directory: str = output_directory
        self.file_list: List[str] = file_list
        self.installer_name: str = installer_name

    def create_installer(self) -> None:
        """
        Creates an MSI installer.

        This method handles the logic for generating an MSI installer. It checks
        for the presence of required files and the installer name, and then proceeds
        to compile the MSI installer using WiX Toolset.
        """
        if not self.file_list:
            print("No files selected. Please select files to include in the installer.")
            return

        if not self.installer_name:
            print("Please enter a name for the MSI file.")
            return

        msi_script_path = os.path.join(self.output_directory, "installer.wxs")
        with open(msi_script_path, "w") as msi_script_file:
            msi_script_file.write(self.generate_msi_script())

        wixobj_file_path = os.path.join(self.output_directory, 'installer.wixobj')

        candle_command = [candle_exe_path, msi_script_path, '-o', wixobj_file_path]
        flyweight = InstallerFlyweightFactory.get_flyweight("MSI")
        flyweight.compile_script(candle_command)

        if not os.path.exists(wixobj_file_path):
            print(".wixobj file not created. Compilation may have failed.")
            return

        light_command = [light_exe_path, wixobj_file_path, '-o', os.path.join(self.output_directory, self.installer_name + '.msi')]
        flyweight.compile_script(light_command)

        print("MSI installer created successfully in the output directory.")

    def generate_msi_script(self) -> str:
        """
        Generates an XML script for MSI installation using WiX Toolset.

        Returns:
            str: A string containing the WiX XML script necessary to create the MSI installer.
        """
        new_guid = str(uuid.uuid4()).upper()
        components_xml = self.generate_components()
        component_refs_xml = self.generate_component_refs()

        msi_script = f"""<?xml version="1.0" encoding="UTF-8"?>
                        <Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
                            <Product Id="*" Name="{self.installer_name}" Language="1033" Version="1.0.0.0" Manufacturer
                            ="MyCompany" UpgradeCode="{new_guid}">       
                                <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
                                <Media Id="1" Cabinet="media1.cab" EmbedCab="yes" />
                                <Directory Id="TARGETDIR" Name="SourceDir">
                                    <Directory Id="ProgramFilesFolder">
                                        <Directory Id="INSTALLFOLDER" Name="{self.installer_name}">
                                            {components_xml}
                                        </Directory>
                                    </Directory>
                                </Directory>
                                <Feature Id="ProductFeature" Title="{self.installer_name}" Level="1">
                                    {component_refs_xml}
                                </Feature>
                            </Product>
                        </Wix>
                        """
        return msi_script

    def generate_components(self) -> str:
        """
        Generates XML components for each file to be included in the MSI installer.

        This method iterates over the file list and creates an XML component for each file,
        which is then used in the WiX script.

        Returns:
            str: A string containing XML components for the installer script.
        """
        components_xml = ""
        for file in self.file_list:
            file_id = os.path.basename(file)
            source_path = os.path.join(self.source_directory, file)
            component_xml = f"""
            <Component Id="{file_id}" Guid="{str(uuid.uuid4())}">
                <File Id="{file_id}" Source="{source_path}" KeyPath="yes" />
            </Component>
            """
            components_xml += component_xml
        return components_xml

    def generate_component_refs(self) -> str:
        """
        Generates XML component references for the WiX script.

        This method creates a reference for each component in the installer script,
        ensuring that each file is correctly included in the MSI package.

        Returns:
            str: A string containing XML component references.
        """
        component_refs_xml = ""
        for file in self.file_list:
            file_id = os.path.basename(file)
            component_ref_xml = f"<ComponentRef Id=\"{file_id}\" />"
            component_refs_xml += component_ref_xml
        return component_refs_xml

    def compile_msi_script(self, msi_script_path: str) -> None:
        """
        Compiles the MSI script using WiX Toolset's candle and light applications.

        This method first uses 'candle' to compile the WiX script into an object file and
        then uses 'light' to link and bind the object file into an MSI package.

        Args:
            msi_script_path (str): Path to the WiX script file.
        """
        candle_exe_path = r'C:\Program Files (x86)\WiX Toolset v3.14\bin\candle.exe'
        light_exe_path = r'C:\Program Files (x86)\WiX Toolset v3.14\bin\light.exe'

        wixobj_file_path = os.path.join(self.output_directory, 'installer.wixobj')

        candle_command = [candle_exe_path, msi_script_path, '-o', wixobj_file_path]
        candle_result = subprocess.run(candle_command, capture_output=True, text=True)
        if candle_result.returncode != 0:
            print(f"Candle error output: {candle_result.stderr}")
            return
        print(f"Candle output: {candle_result.stdout}")

        if not os.path.exists(wixobj_file_path):
            print(".wixobj file not created. Compilation may have failed.")
            return

        light_command = [light_exe_path, wixobj_file_path, '-o', os.path.join(self.output_directory, self.installer_name + '.msi')]
        light_result = subprocess.run(light_command, capture_output=True, text=True)
        if light_result.returncode != 0:
            print(f"Light error output: {light_result.stderr}")
            return
        print(f"Light output: {light_result.stdout}")
        print("MSI installer created successfully in the output directory.")
