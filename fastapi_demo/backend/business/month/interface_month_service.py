from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class IMonthService(ABC):
    @abstractmethod
    def get_months(self) -> List[int]:
        pass