from app.application.auth.get_current_user import GetCurrentUser
from app.application.auth.login import LoginUser
from app.application.auth.register import RegisterUser
from app.application.listings.archive_listing import ArchiveListing
from app.application.listings.create_listing import CreateListing
from app.application.listings.list_catalog import ListCatalog
from app.application.listings.publish_listing import PublishListing
from app.application.listings.update_listing import UpdateListing
from app.application.payments.confirm_mock_payment import ConfirmMockPayment
from app.application.payments.handle_webhook import HandleWebhook
from app.application.payments.initiate_topup import InitiateTopup
from app.application.referrals.apply_referral import ApplyReferral
from app.application.referrals.get_referral_stats import GetReferralStats
from app.application.referrals.reward_referral import RewardReferral
from app.application.wallet.get_balance import GetBalance
from app.application.wallet.list_transactions import ListTransactions
from app.application.wallet.post_ledger_entry import PostLedgerEntry
from app.config import settings
from app.infrastructure.auth.jwt_token_service import JwtTokenService
from app.infrastructure.auth.local_auth_provider import LocalAuthProvider
from app.infrastructure.payments.mock_yoomoney_provider import MockYooMoneyProvider
from app.infrastructure.payments.provider_registry import PaymentProviderRegistry
from app.infrastructure.payments.yoomoney_provider import YooMoneyProvider
from app.infrastructure.repositories.category_repo import MongoCategoryRepository
from app.infrastructure.repositories.listing_repo import MongoListingRepository
from app.infrastructure.repositories.payment_intent_repo import MongoPaymentIntentRepository
from app.infrastructure.repositories.referral_repo import MongoReferralRepository
from app.infrastructure.repositories.transaction_repo import MongoTransactionRepository
from app.infrastructure.repositories.user_repo import MongoUserRepository
from app.infrastructure.storage.local_file_storage import LocalFileStorage
from app.domain.ports.token_service import TokenService


class Container:
    def __init__(self) -> None:
        self.users = MongoUserRepository()
        self.listings = MongoListingRepository()
        self.transactions = MongoTransactionRepository()
        self.payment_intents = MongoPaymentIntentRepository()
        self.referrals = MongoReferralRepository()
        self.categories = MongoCategoryRepository()
        self.tokens: TokenService = JwtTokenService()
        self.auth = LocalAuthProvider(self.users)
        self.storage = LocalFileStorage()
        self.payment_providers = PaymentProviderRegistry()
        if settings.yoomoney_shop_id and settings.yoomoney_secret:
            self.payment_providers.register(YooMoneyProvider())
        else:
            self.payment_providers.register(MockYooMoneyProvider())

        self.ledger = PostLedgerEntry(self.users, self.transactions)
        self.apply_referral = ApplyReferral(self.users, self.referrals)
        self.reward_referral = RewardReferral(self.referrals, self.ledger)
        self.register_user = RegisterUser(
            self.auth, self.tokens, self.users, self.apply_referral
        )
        self.login_user = LoginUser(self.auth, self.tokens)
        self.get_current_user = GetCurrentUser(self.users)
        self.get_balance = GetBalance(self.users)
        self.list_transactions = ListTransactions(self.transactions)
        self.create_listing = CreateListing(self.listings, self.categories)
        self.publish_listing = PublishListing(
            self.listings, self.ledger, self.reward_referral
        )
        self.list_catalog = ListCatalog(self.listings)
        self.update_listing = UpdateListing(self.listings)
        self.archive_listing = ArchiveListing(self.listings)
        self.initiate_topup = InitiateTopup(self.payment_intents, self.payment_providers)
        self.handle_webhook = HandleWebhook(
            self.payment_intents, self.payment_providers, self.ledger
        )
        self.confirm_mock_payment = ConfirmMockPayment(
            self.payment_intents, self.handle_webhook
        )
        self.get_referral_stats = GetReferralStats(self.users, self.referrals)


container = Container()
