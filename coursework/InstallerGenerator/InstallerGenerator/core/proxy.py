import logging
from typing import Any
from .creators.abc_creator import InstallerCreator
from .logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class InstallerCreatorProxy(InstallerCreator):
    """
    A proxy class for creating installers, allowing for additional functionality.

    This class acts as a proxy for creating installers, enabling the logging of creation events and handling errors.
    """

    def __init__(self, real_creator: InstallerCreator, installer_type: str):
        """
        Initialize the InstallerCreatorProxy.

        Args:
            real_creator (InstallerCreator): The real installer creator to delegate the creation to.
            installer_type (str): The type of installer being created (e.g., 'MSI' or 'EXE').
        """
        self._real_creator = real_creator
        self._installer_type = installer_type

    def create_installer(self) -> Any:
        """
        Create the installer and log creation events.

        This method delegates the creation of the installer to the real creator while logging events.

        Returns:
            Any: The result of the installer creation process.

        Raises:
            Exception: If an error occurs during the installer creation process.
        """
        logging.info(f"Proxy: Starting to create {self._installer_type} installer.")

        try:
            result = self._real_creator.create_installer()
            logging.info(f"Proxy: {self._installer_type} installer created successfully.")
            return result
        except Exception as e:
            logging.error(f"Proxy: Error occurred while creating {self._installer_type} installer - {e}")
            raise
