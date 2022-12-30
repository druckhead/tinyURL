import os.path
# from os import curdir
# from os.path import join
from json import load, dump
from dotenv import load_dotenv
from requests import exceptions, post, patch, get, delete

load_dotenv()


class DruckUrl:
    _url = "https://api.tinyurl.com"
    __key = os.getenv("API_KEY")
    __json_path = "shortened_urls.json"

    def __init__(self) -> None:
        if not os.path.exists(os.path.join(os.curdir, self.__json_path)):
            self._shortened_urls = {}
        else:
            self._shortened_urls = self._load()

    def _save(self):
        path = os.path.join(os.curdir, self.__json_path)
        with open(path, 'w') as out_file:
            dump(self._shortened_urls, out_file)

    def _load(self) -> dict:
        path = os.path.join(os.curdir, self.__json_path)
        with open(path, 'r') as write_file:
            shortened_urls = load(write_file)
        return shortened_urls

    def _update_my_urls(self, response_json: dict[str, dict[str | dict]]) -> None:
        tiny_url = response_json.get("data").get("tiny_url")
        self._shortened_urls[tiny_url] = response_json

    def create(self, long_url: str):
        request_body = {
            "url": long_url,
            "domain": "tinyurl.com",
            "alias": "",
            "tags": "",
            "expires_at": "",
        }

        request_url = f"{self._url}/create?api_token={self.__key}"
        response = post(request_url, json=request_body)

        if response.status_code == 200:
            response_as_json = response.json()
            self._update_my_urls(response_as_json)
            self._save()
            return response_as_json

        raise exceptions.RequestException(response.text)

    def update(self):
        request_body = {
            "domain": "my-custom-domain.com",
            "alias": "promotion2020",
            "new_domain": "tiny.one",
            "new_alias": "promotion2021",
            "new_stats": True,
            "new_tags": [
                "new tag",
                "example"
            ],
            "new_expires_at": "P10DT4H"
        }

        request_url = f"{self._url}/update?api_token={self.__key}"
        response = patch(request_url, json=request_body)

        if response.status_code == 200:
            response_as_json = response.json()
            self._update_my_urls(response_as_json)
            self._save()
            return response_as_json

        raise exceptions.RequestException(response.text)

    def change(self):
        request_body = {
            "url": "",
            "domain": "",
            "alias": ""
        }

        request_url = f"{self._url}/change?api_token={self.__key}"
        response = patch(request_url, json=request_body)

        if response.status_code == 200:
            response_as_json = response.json()
            # self._update_my_urls(response_as_json)
            # self._save()
            return response_as_json

        raise exceptions.RequestException(response.text)

    def get_info(self, domain: str, alias: str):
        request_body = {
            "domain": domain,
            "alias": alias
        }

        request_url = f"{self._url}/alias/{domain}/{alias}?api_token={self.__key}"
        response = get(request_url, json=request_body)

        if response.status_code == 200:
            response_as_json = response.json()
            # self._update_my_urls(response_as_json)
            # self._save()
            return response_as_json

        raise exceptions.RequestException(response.text)

    def delete(self, domain: str, alias: str):
        request_body = {
            "domain": domain,
            "alias": alias
        }

        request_url = f"{self._url}/alias/{domain}/{alias}?api_token={self.__key}"
        response = delete(request_url, json=request_body)

        if response.status_code == 200:
            response_as_json = response.json()
            # self._update_my_urls(response_as_json)
            # self._save()
            return response_as_json

        raise exceptions.RequestException(response.text)

    def archive(self, domain: str, alias: str):
        request_body = {
            "domain": domain,
            "alias": alias
        }

        request_url = f"{self._url}/archive?api_token={self.__key}"
        response = patch(request_url, json=request_body)


if __name__ == '__main__':
    dr = DruckUrl()
    print(dr.create("https://osxdaily.com/2021/12/17/check-sha256-hash-mac/"))
