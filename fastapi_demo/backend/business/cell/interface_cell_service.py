from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class ICellService(ABC):
    @abstractmethod
    def get_cells(self) -> List[int]:
        pass