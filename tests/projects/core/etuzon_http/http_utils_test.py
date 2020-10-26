import unittest
import requests_mock
from requests import Response
from projects.core.etuzon_http.http_utils import HttpUtil
from projects.core.exceptions.http_exceptions import HttpResponseNotJson


class HttpUtilTests(unittest.TestCase):
    RESPONSE_TEXT = "{\"key1\":39.30,\"key2\":\"value2\"," \
                    "\"key3\":null,\"key4\":true}"

    def test_1_convert_http_response_to_dict(self):
        response = Response()
        response._content = HttpUtilTests.RESPONSE_TEXT.encode()
        response_dict = HttpUtil.convert_http_json_response_to_dict(response)
        self._verify_response_dict(response_dict)

    def test_2_convert_none_json_http_response(self):
        response = Response()
        response._content = "123456".encode()

        with self.assertRaises(HttpResponseNotJson):
            HttpUtil.convert_http_json_response_to_dict(response)

    def test_3_convert_empty_http_response(self):
        response = Response()
        response._content = "".encode()

        with self.assertRaises(HttpResponseNotJson):
            HttpUtil.convert_http_json_response_to_dict(response)

    def test_4_convert_none_http_response(self):
        response = Response()
        response._content = None

        with self.assertRaises(HttpResponseNotJson):
            HttpUtil.convert_http_json_response_to_dict(response)

    def test_5_send_http_get_and_receive_response_to_dict(self):
        url = "http://test.com"
        with requests_mock.Mocker() as m:
            m.get(url, text=self.RESPONSE_TEXT)
            response_dict = \
                HttpUtil.send_get_request_receive_json_response(url)
            self._verify_response_dict(response_dict)

    def _verify_response_dict(self, response_dict: dict):
        self.assertTrue(isinstance(response_dict, dict))
        self.assertTrue(response_dict["key1"] == 39.30)
        self.assertTrue(response_dict["key2"] == "value2")
        self.assertTrue(response_dict["key3"] is None)
        self.assertTrue(response_dict["key4"])


if __name__ == '__main__':
    unittest.main()
