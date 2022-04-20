from dataclasses import dataclass
from .model import Model, ModelProtocol
from typing import Protocol, Optional
from .connection import terminations

__all__ = (
    'TerminationProtocol',
    'Termination'
)

class TerminationProtocol(ModelProtocol, Protocol):
    _id: str
    username: str
    reason: str

@dataclass
class Termination(Model[TerminationProtocol], collection = terminations):
    _id: Optional[str] = None
    username: Optional[str] = None
    reason: Optional[str] = None