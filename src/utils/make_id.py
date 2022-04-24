import random
import string
from .._typing import PostID

__all__ = ("make_id",)

def make_id() -> PostID:
   """Generate an ID for a post."""
   return PostID(
       ''.join(
           random.choice(string.ascii_letters) for _ in range(50)
        )
    )