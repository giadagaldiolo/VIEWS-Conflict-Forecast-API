from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class IMonthService(ABC):
    """
    Interface for services related to month data.

    Defines the contract for retrieving available month identifiers.
    """
    
    @abstractmethod
    def get_months(self) -> List[int]:
        """
        Retrieve a list of month IDs.

        Returns:
            List[int]: List of unique month identifiers, typically in YYYYMM format.
        """
        pass