from app.domain.ports.payment_provider import PaymentProvider


class PaymentProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, PaymentProvider] = {}

    def register(self, provider: PaymentProvider) -> None:
        self._providers[provider.provider_id] = provider

    def get(self, provider_id: str) -> PaymentProvider:
        provider = self._providers.get(provider_id)
        if not provider:
            raise KeyError(f"Payment provider '{provider_id}' not registered")
        return provider
