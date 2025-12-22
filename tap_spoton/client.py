"""REST client handling, including SpotOnStream base class."""

from typing import Any, Dict, Optional

import requests
from hotglue_tap_sdk.streams import RESTStream
from memoization import cached

from tap_spoton.auth import SpotOnAuthenticator


class SpotOnStream(RESTStream):
    """SpotOn stream class."""

    url_base = "https://api.spoton.com/"

    @property
    @cached
    def authenticator(self) -> SpotOnAuthenticator:
        """Return a new authenticator object."""
        return SpotOnAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        previous_token = previous_token or 1
        if response.json().get("pagination").get("total_pages") > previous_token:
            return previous_token + 1
        else:
            return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_time(context)
            params["last_updated_from"] = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return params
