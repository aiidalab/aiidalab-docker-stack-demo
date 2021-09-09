from typing import Tuple
from oauthenticator.generic import GenericOAuthenticator

from tornado.httpclient import HTTPRequest, AsyncHTTPClient

class MarketplaceOAuthenticator(GenericOAuthenticator):
    """A GenericOAuthenticator with assigned LoginHandler containing Marketplace specific urls"""

    async def _fetch_user_details(self, access_token):
        """Get user details from Marketplace user-service API from user ID"""
        import json

        http_client = AsyncHTTPClient()
        headers = {
            "Accept": "application/json",
            "User-Agent": "JupyterHub",
            "Authorization": f"Bearer {access_token}",
        }

        # Use GET request method
        req = HTTPRequest(
            "https://{{ marketplace_host }}/user-service/userinfo",
            method="GET",
            headers=headers,
            validate_cert=False,
        )
        resp = await http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))

        return resp_json

    async def authenticate(self, handler, data=None):
        """Overloads authentication service to include an additional call to marketplace user-service API."""
        resp_json = await super().authenticate(handler, data=data)

        # Get full user details
        access_token = resp_json['auth_state']['access_token']
        refresh_token = resp_json['auth_state']['refresh_token']
        user_json = await self._fetch_user_details(access_token)

        # Update real username and store additional details in in auth_state
        resp_json['name'] = user_json['name']
        resp_json['auth_state']['oauth_user'].update(user_json)

        return resp_json
