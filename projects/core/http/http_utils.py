import urllib.request
from ast import literal_eval

import requests

from projects.core.exceptions.http_exceptions import HttpResponseNotJson


class HttpUtil:
    @staticmethod
    def send_get_request_receive_json_response(url, headers=None) -> dict:
        response = requests.request("GET", url, headers=headers)
        response_str = response.text.replace(":null,", ":None,").\
            replace(":true,", ":True,").replace(":false,", ":False,")

        try:
            return literal_eval(response_str)
        except ValueError as e:
            if response_str is None:
                response_str = ""
            raise HttpResponseNotJson(response_str)
