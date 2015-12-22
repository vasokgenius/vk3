import requests
import json
import urllib
from ..settings import *


AUTH_URL = 'https://oauth.vk.com/authorize?client_id={0}&scope={1}&display={2}\
&response_type=token&revoke=1&redirect_uri={3}'\
    .format(VK_CLIENT_ID, 'photos,video,docs,groups,offline','page', VK_REDIRECT_URI)


class VkClient(object):

    def __init__(self, access_token):
        super(VkClient, self).__init__()
        self.access_token = access_token
        self.requests_session = requests.Session()

    def __call__(self, method_name, **method_kwargs):
        response = self.method_request(method_name, **method_kwargs)
        return response

    def stringify_values(self, method_kwargs):
        stringified_method_kwargs = ''
        for key in method_kwargs:
            stringified_method_kwargs = stringified_method_kwargs + \
                (str(key) + '=' + str(method_kwargs[key]) + '&')
        return stringified_method_kwargs

    def method_request(self, method_name, timeout=None, **method_kwargs):
        str_kwargs = self.stringify_values(method_kwargs)
        url = 'https://api.vk.com/method/' + method_name + '?' + str_kwargs + \
            'access_token=' + self.access_token + '&lang=ru&v=' + VK_V # +'&test_mode=1'
        response = self.requests_session.post(url)
        json_response = json.loads(response.text)
        try:
            return json_response['response']
        except KeyError:
            try:
                error_code = json_response['error']['error_code']
                error_msg = json_response['error']['error_msg']
                raise VkError(json_response['error']['error_code'], json_response['error']['error_msg'])
            except KeyError:
                return json_response

    def __getattr__(self, method_name):
        return APIMethod(self, method_name)


class APIMethod(object):

    def __init__(self, api_session, method_name):
        self._api_session = api_session
        self._method_name = method_name

    def __getattr__(self, method_name):
        return APIMethod(self._api_session, self._method_name + '.' + method_name)

    def __call__(self, **method_kwargs):
        return self._api_session(self._method_name, **method_kwargs)

class VkError(Exception):
	def __init__(self, code, message):
		self.code = code
		self.message = message

	def __str__(self):
		return ('VK ERROR [{0}]:{1}').format(self.code, self.message)