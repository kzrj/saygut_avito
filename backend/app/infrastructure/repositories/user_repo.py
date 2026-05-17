from datetime import datetime

from beanie import PydanticObjectId

from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.domain.value_objects.auth_identity import AuthIdentity
from app.infrastructure.db.documents.user_doc import IdentityEmbedded, UserDoc
from app.infrastructure.db.mappers import user_to_entity


class MongoUserRepository(UserRepository):
    async def get_by_id(self, user_id: str) -> User | None:
        doc = await UserDoc.get(PydanticObjectId(user_id))
        return user_to_entity(doc) if doc else None

    async def get_by_email(self, email: str) -> User | None:
        doc = await UserDoc.find_one(UserDoc.email == email.lower())
        return user_to_entity(doc) if doc else None

    async def get_by_phone(self, phone: str) -> User | None:
        doc = await UserDoc.find_one(UserDoc.phone == phone)
        return user_to_entity(doc) if doc else None

    async def get_by_referral_code(self, code: str) -> User | None:
        doc = await UserDoc.find_one(UserDoc.referral_code == code.upper())
        return user_to_entity(doc) if doc else None

    async def save(self, user: User) -> User:
        oid = PydanticObjectId(user.id) if user.id else None
        if oid:
            doc = await UserDoc.get(oid)
            if not doc:
                doc = UserDoc(id=oid)
        else:
            doc = UserDoc()

        doc.email = user.email.lower() if user.email else None
        doc.phone = user.phone
        doc.password_hash = user.password_hash
        doc.display_name = user.display_name
        doc.wallet_balance = user.wallet_balance
        doc.referral_code = user.referral_code
        doc.referred_by_id = user.referred_by_id
        doc.identities = [
            IdentityEmbedded(provider=i.provider, external_id=i.external_id, meta=i.meta)
            for i in user.identities
        ]
        doc.role = user.role
        doc.status = user.status
        doc.updated_at = datetime.utcnow()
        if not doc.created_at:
            doc.created_at = user.created_at
        await doc.save()
        return user_to_entity(doc)

    async def update_balance(self, user_id: str, new_balance: int) -> None:
        doc = await UserDoc.get(PydanticObjectId(user_id))
        if doc:
            doc.wallet_balance = new_balance
            doc.updated_at = datetime.utcnow()
            await doc.save()
