import requests

from exceptions.ApiException import ApiException


class CaRestClient:

    def __init__(self, ca_server_url, csr=None):
        self.ca_server_url = ca_server_url
        self.csr = csr

    def test_connection(self):
        response = requests.get(self.ca_server_url)
        if response.status_code != 200:
            raise ApiException(response.status_code)
        return response
