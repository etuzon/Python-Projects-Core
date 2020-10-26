from ast import literal_eval

import requests
from requests import Response
from requests.auth import HTTPBasicAuth
from projects.core.exceptions.http_exceptions import HttpResponseNotJson


class HttpUtil:
    @staticmethod
    def send_get_request_receive_json_response(
            url, headers=None, basic_auth: HTTPBasicAuth = None) -> dict:
        response = requests.request("GET", url, headers=headers,
                                    auth=basic_auth)
        return HttpUtil.convert_http_json_response_to_dict(response)

    @staticmethod
    def convert_http_json_response_to_dict(response: Response):
        if response.text is None:
            HttpResponseNotJson("Response body was not found")

        response_str = response.text.replace("\":null", "\":None") \
                                    .replace("\": null", "\":None") \
                                    .replace("\":true", "\":True") \
                                    .replace("\": true", "\":True") \
                                    .replace("\":false", "\":False") \
                                    .replace("\": false", "\":False")

        try:
            dict_result = literal_eval(response_str)

            if not isinstance(dict_result, dict):
                HttpUtil._raise_http_response_not_json_exception(response_str)

            return literal_eval(response_str)
        except (ValueError, SyntaxError):
            HttpUtil._raise_http_response_not_json_exception(response_str)

    @staticmethod
    def _raise_http_response_not_json_exception(response_str):
        if response_str is None:
            response_str = ""
        raise HttpResponseNotJson(response_str)
