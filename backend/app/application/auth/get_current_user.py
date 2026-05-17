from app.domain.entities.user import User
from app.domain.exceptions import NotFoundError
from app.domain.ports.user_repository import UserRepository


class GetCurrentUser:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: str) -> User:
        user = await self._users.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
