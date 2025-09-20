from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class ICountryService(ABC):
    @abstractmethod
    def get_countries(self) -> List[int]:
        pass