"""SpotOn Authentication."""


from hotglue_tap_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class SpotOnAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for SpotOn."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the SpotOn API."""
        return {
            "scope": self.oauth_scopes,
            "grant_type": "client_credentials",
        }

    def request_auth(self) -> tuple[str, str]:
        """Return the authentication credentials for the request."""
        return (self.config["username"], self.config["password"])

    @classmethod
    def create_for_stream(cls, stream) -> "SpotOnAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="https://api.spoton.com/oauth2/v1/token",
            oauth_scopes="reporting:orders:read business:all:read",
        )
