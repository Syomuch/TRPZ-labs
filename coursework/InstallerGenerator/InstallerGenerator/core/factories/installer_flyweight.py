from .flyweight import InstallerFlyweight
from typing import Dict

class InstallerFlyweightFactory:
    """
    Factory for managing and retrieving installer flyweights.

    This class acts as a flyweight factory responsible for creating and managing installer flyweights.
    Installer flyweights are shared objects used to optimize memory usage when creating similar installers.
    """
    _flyweights: Dict[str, InstallerFlyweight] = {}

    @classmethod
    def get_flyweight(cls, key: str) -> InstallerFlyweight:
        """
        Retrieve an installer flyweight for the given key.

        If a flyweight with the specified key exists, it is returned; otherwise, a new one is created.

        Args:
            key (str): The key used to identify the installer flyweight.

        Returns:
            InstallerFlyweight: An installer flyweight instance.
        """
        if not cls._flyweights.get(key):
            cls._flyweights[key] = InstallerFlyweight(key)
        return cls._flyweights[key]
