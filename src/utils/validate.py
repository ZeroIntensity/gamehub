from typing import Dict, Union, NoReturn
from strawberry.types import Info
from .exception import exception

__all__ = ('validate',)

def validate(info: Info, conds: Dict[bool, str]) -> Union[None, NoReturn]:
    """Function for validating conditions in a GraphQL resolver."""
    for key, value in conds.items():
        if key:
            exception(info, value)

