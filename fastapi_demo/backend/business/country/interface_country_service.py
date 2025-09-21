from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class ICountryService(ABC):
    """
    Interface for services related to country data.

    Any implementation must provide a method to retrieve country IDs.
    """

    @abstractmethod
    def get_countries(self) -> List[int]:
        """
        Retrieve a list of country IDs.

        Returns:
            List[int]: List of unique country identifiers.
        """
        pass