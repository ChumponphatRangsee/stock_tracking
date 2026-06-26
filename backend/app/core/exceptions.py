class APIQuotaExceededError(Exception):
    """Raised when an API provider's quota is exhausted."""
    def __init__(self, provider: str, message: str = "API quota exceeded"):
        self.provider = provider
        self.message = f"{message} for provider: {provider}"
        super().__init__(self.message)

class APIProviderError(Exception):
    """Raised when an external API provider returns an error."""
    pass