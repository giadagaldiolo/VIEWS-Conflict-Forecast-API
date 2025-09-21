from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class ICellService(ABC):
    """
    Interface for cell-related services.

    Defines methods that any cell service implementation must provide.
    """

    @abstractmethod
    def get_cells(self) -> List[int]:
        """
        Retrieve a list of priogrid IDs.

        Returns:
            List[int]: List of priogrid IDs.
        """
        pass