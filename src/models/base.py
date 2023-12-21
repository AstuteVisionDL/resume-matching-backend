from typing import List
from abc import ABC, abstractmethod

class BaseJobSimilarity(ABC):
    """
    Base class for detection
    """

    @abstractmethod
    def find_similarity(self, word1: str, word2: str) -> float:
        """
        Detects signs on image
        """
        raise NotImplementedError(
            "This method should be implemented in child class"
        )