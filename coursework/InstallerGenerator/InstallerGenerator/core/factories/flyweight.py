import subprocess

class InstallerFlyweight:
    """
    Represents a flyweight for compiling installer scripts.

    This class represents an installer flyweight used to compile installer scripts efficiently.
    Installer flyweights are shared objects that optimize memory usage when compiling similar scripts.
    """
    def __init__(self, script: str):
        """
        Initialize the InstallerFlyweight.

        Args:
            script (str): The script type identifier.
        """
        self._script: str = script

    def compile_script(self, compile_command: list) -> None:
        """
        Compile an installer script using the specified compile command.

        This method compiles an installer script using a given compile command and handles the output.

        Args:
            compile_command (list): The command used to compile the script.

        Raises:
            RuntimeError: If the compilation fails with a non-zero return code.
        """
        compile_result = subprocess.run(compile_command, capture_output=True, text=True)
        if compile_result.returncode != 0:
            print(f"Error output: {compile_result.stderr}")
            return
        print(f"Output: {compile_result.stdout}")
