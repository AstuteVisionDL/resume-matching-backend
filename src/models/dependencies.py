from src.models.e5 import E5
from src.models.base import BaseJobSimilarity


def get_actual_model() -> BaseJobSimilarity:
    """Dependency for returning actual detector"""
    return E5()