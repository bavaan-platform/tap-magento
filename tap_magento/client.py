"""REST client handling, including MagentoStream base class."""

import requests
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Callable, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.authenticators import BearerTokenAuthenticator
from datetime import datetime
import backoff


logging.getLogger("backoff").setLevel(logging.CRITICAL)

class MagentoStream(RESTStream):
    """Magento stream class."""
    access_token = None
    expires_in = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        store_url = self.config["store_url"]
        return f"{store_url}/rest/V1"

    records_jsonpath = "$.items[*]"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        if  self.config.get('username') and self.config.get('password') is not None:   
            token = self.get_token()
        else:
            token = self.config.get('api_key')    
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=token
        )

    def get_token(self):
        now = round(datetime.utcnow().timestamp())
        if not self.access_token:
            s = requests.Session()
            payload = {
                "Content-Type": "application/json",
                "username": self.config.get('username'),
                "password": self.config.get('password'),
                }
            try:
                login = s.post(f"{self.config['store_url']}/index.php/rest/V1/integration/admin/token", json=payload)
                login.json()
                login.raise_for_status()
            except:
                login = s.post(f"{self.config['store_url']}/rest/V1/integration/admin/token", json=payload)
            login.raise_for_status()

            self.access_token = login.json()

        return self.access_token

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {
            "Content-Type": "application/json",
            }
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        next_page_token = None
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_token = first_match
        elif response.status_code == 404:
            return None
        else:
            json_data = response.json()
            total_count = json_data.get("total_count", 0)
            if json_data.get("search_criteria"):
                current_page = json_data.get("search_criteria").get("current_page")
            else:
                current_page = 1    
            if total_count > current_page * 300:
                next_page_token = current_page + 1
        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {}
        params["searchCriteria[pageSize]"] = 300
        if not next_page_token:
            params["searchCriteria[currentPage]"] = 1
        else:
            params["searchCriteria[currentPage]"] = next_page_token
        
        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            if start_date is not None:
                start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
                params["sort"] = "asc"
                params["searchCriteria[filterGroups][0][filters][0][field]"] = self.replication_key
                params["searchCriteria[filterGroups][0][filters][0][value]"] = start_date
                params["searchCriteria[filterGroups][0][filters][0][conditionType]"] = "gt"
            params["order_by"] = self.replication_key
        return params

    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response."""
        if response.status_code == 404:
            pass
        elif 400 <= response.status_code < 500:
            msg = (
                f"{response.status_code} Client Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise FatalAPIError(msg)

        elif 500 <= response.status_code < 600:
            msg = (
                f"{response.status_code} Server Error: "
                f"{response.reason} for path: {self.path}"
            )
            raise RetriableAPIError(msg)

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        if response.status_code == 404:
            return []
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())


    def request_decorator(self, func: Callable) -> Callable:
        """Instantiate a decorator for handling request failures.
        """
        decorator: Callable = backoff.on_exception(
            backoff.expo,
            (
                RetriableAPIError,
                requests.exceptions.ReadTimeout,
                ConnectionError
            ),
            max_tries=5,
            factor=2,
        )(func)
        return decorator

