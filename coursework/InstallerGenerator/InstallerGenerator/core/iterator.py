from typing import List, Any

class FileListIterator:
    """
    An iterator class to iterate over a list of files.

    Attributes:
        _file_list (List[Any]): The list of files to iterate over.
        _index (int): The current index in the file list.
    """
    def __init__(self, file_list: List[Any]):
        """
        Initializes the FileListIterator with a list of files.

        Args:
            file_list (List[Any]): The list of files to iterate over.
        """
        self._file_list: List[Any] = file_list
        self._index: int = 0

    def __next__(self) -> Any:
        """
        Returns the next file in the list.

        Raises:
            StopIteration: If the end of the file list is reached.
        """
        if self._index < len(self._file_list):
            result: Any = self._file_list[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration
