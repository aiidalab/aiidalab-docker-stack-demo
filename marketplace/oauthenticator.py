from typing import Tuple
from oauthenticator.generic import GenericOAuthenticator

from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from jupyterhub.handlers.base import BaseHandler

# add route for terms & conditions
class TermsConditionsHandler(BaseHandler):

    def get(self): # pylint: disable=arguments-differ
        """Terms and conditions"""
        # Note: This placeholder serves a demonstration for adding
        # additional routes and associated handlers.
        self.write("This is the terms and conditions of this service.")
    
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
        user_json = await self._fetch_user_details(access_token)

        # Update real username and store additional details in in auth_state
        resp_json['name'] = user_json['name']
        resp_json['auth_state']['oauth_user'].update(user_json)

        return resp_json

    async def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = await user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return
        spawner.environment['MP_HOST'] = "https://{{ marketplace_host }}"
        spawner.environment['MP_ACCESS_TOKEN'] = auth_state['access_token']
        spawner.environment['MP_REFRESH_TOKEN'] = auth_state['refresh_token']
