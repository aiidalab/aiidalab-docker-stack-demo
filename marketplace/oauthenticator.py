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

    async def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = await user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return
        spawner.environment['MP_HOST'] = "https://{{ marketplace_host }}"
        spawner.environment['MP_ACCESS_TOKEN'] = auth_state['access_token']
        spawner.environment['MP_REFRESH_TOKEN'] = auth_state['refresh_token']
