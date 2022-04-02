import strawberry
from ..db import GameModel, GameInput, FoundUser
from .permissions import Authenticated
from ..utils import check_perms
from strawberry.types import Info

@strawberry.field(
    description = "Create a game.",
    permission_classes = [Authenticated]
)
def create_game(info: Info, data: GameInput) -> str:
    user: FoundUser = info.context.user
    check_perms(user.account_type, 'admin')

    model = GameModel(name = data.name)

    if model.exists():
        raise Exception(f'Game "{data.name}" already exists.')
    
    model.data = data.data
    model.save()

    return f'Created game "{data.name}"'
