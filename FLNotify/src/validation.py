"""Baseline of validation models."""
from abc import ABC, abstractmethod
from typing import List


class ValidationModel(ABC):
    """Base class for validations"""
    def validate_all_clients(self, all_results: List[List[float]]) -> List[int]:
        """Returns a list of indexes which are the malicious_clients.""" 
        malicious_clients = []
        # assume results are already in the correct order
        for index, result in enumerate(all_results):
            if not self.validate_client(result):
                malicious_clients.append(index)
        return malicious_clients

    @abstractmethod
    def validate_client(self, client_results: List[float]) -> bool:
        """Returns a boolean, True represents the results are valid, False are malicious."""


class AlwaysFailValidation(ValidationModel):
    """Always returns a failure on results validation"""
    def validate_client(self, client_results: List[float]) -> bool:
        return False


class AlwaysPassValidation(ValidationModel):
    """Always returns a pass on results validation"""
    def validate_client(self, client_results: List[float]) -> bool:
        return True
