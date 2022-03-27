from typing import Dict, Union, NoReturn

__all__ = ['validate']

def validate(conds: Dict[bool, str]) -> Union[None, NoReturn]:
    """Function for validating conditions in a GraphQL resolver."""
    for key, value in conds.items():
        if key:
            raise Exception(value)

