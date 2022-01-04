import json
import base64
from typing import Tuple
from urllib.parse import urlencode

from oauthenticator.generic import GenericOAuthenticator

from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httputil import url_concat

from jupyterhub.handlers.base import BaseHandler

from traitlets import Unicode

# add route for terms & conditions
class TermsConditionsHandler(BaseHandler):

    def get(self): # pylint: disable=arguments-differ
        """Terms and conditions"""
        # Note: This placeholder serves a demonstration for adding
        # additional routes and associated handlers.
        self.write("This is the terms and conditions of this service.")
    
class MarketplaceOAuthenticator(GenericOAuthenticator):
    """A GenericOAuthenticator with assigned LoginHandler containing Marketplace specific urls"""
    client_id_qe = Unicode(config=True)
    client_secret_qe = Unicode(config=True)

    async def _fetch_user_details(self, access_token):
        """Get user details from Marketplace user-service API from user ID"""
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

        http_client = AsyncHTTPClient()
        code = handler.get_argument("code")

        params = dict(
            redirect_uri=self.get_callback_url(handler),
            code=code,
            grant_type='authorization_code',
        )
        params.update(self.extra_params)

        headers = {"Accept": "application/json", "User-Agent": "JupyterHub"}
        
        qe = True
        if qe:
            self.client_id = self.client_id_qe
            self.client_secret = self.client_secret_qe

        if self.basic_auth:
            b64key = base64.b64encode(
                bytes("{}:{}".format(self.client_id, self.client_secret), "utf8")
            )
            headers.update({"Authorization": "Basic {}".format(b64key.decode("utf8"))})
        
        req = HTTPRequest(
            self.token_url,
            method="POST",
            headers=headers,
            body=urlencode(params),
        )
        token_resp = await http_client.fetch(req)
        token_resp_json = json.loads(token_resp.body.decode('utf8', 'replace'))

        access_token = token_resp_json['access_token']
        token_type = token_resp_json['token_type']

        # Determine who the logged in user is
        headers = {
            "Accept": "application/json",
            "User-Agent": "JupyterHub",
            "Authorization": "{} {}".format(token_type, access_token),
        }
        if self.userdata_url:
            url = url_concat(self.userdata_url, self.userdata_params)
        else:
            raise ValueError("Please set the OAUTH2_USERDATA_URL environment variable")

        if self.userdata_token_method == "url":
            url = url_concat(self.userdata_url, dict(access_token=access_token))

        req = HTTPRequest(url, headers=headers)
        
        http_client = AsyncHTTPClient()
        user_data_resp = await http_client.fetch(req)
        user_data_resp_json = json.loads(user_data_resp.body.decode('utf8', 'replace'))

        if callable(self.username_key):
            name = self.username_key(user_data_resp_json)
        else:
            name = user_data_resp_json.get(self.username_key)
            if not name:
                self.log.error(
                    "OAuth user contains no key %s: %s",
                    self.username_key,
                    user_data_resp_json,
                )
                return

        user_info = {
            'name': name,
            'auth_state': self._create_auth_state(token_resp_json, user_data_resp_json),
        }

        # if self.allowed_groups:
        #     self.log.info(
        #         'Validating if user claim groups match any of {}'.format(
        #             self.allowed_groups
        #         )
        #     )

        #     if callable(self.claim_groups_key):
        #         groups = self.claim_groups_key(user_data_resp_json)
        #     else:
        #         groups = user_data_resp_json.get(self.claim_groups_key)

        #     if not groups:
        #         self.log.error(
        #             "No claim groups found for user! Something wrong with the `claim_groups_key` {}? {}".format(
        #                 self.claim_groups_key, user_data_resp_json
        #             )
        #         )
        #         groups = []

        #     if self.check_user_in_groups(groups, self.allowed_groups):
        #         user_info['admin'] = self.check_user_in_groups(
        #             groups, self.admin_groups
        #         )
        #     else:
        #         user_info = None

        # Get full user details
        access_token = user_info['auth_state']['access_token']
        user_json = await self._fetch_user_details(access_token)

        # Update real username and store additional details in in auth_state
        user_info['name'] = user_json['name']
        user_info['auth_state']['oauth_user'].update(user_json)

        return user_info

    async def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = await user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return
        spawner.environment['MP_ACCESS_TOKEN'] = auth_state['access_token']
        spawner.environment['MP_REFRESH_TOKEN'] = auth_state['refresh_token']
