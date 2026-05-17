from app.domain.exceptions import NotFoundError
from app.domain.ports.user_repository import UserRepository


class GetBalance:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: str) -> int:
        user = await self._users.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user.wallet_balance
