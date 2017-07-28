from json import dumps
from datetime import datetime
from hashlib import md5
from os import path

import requests


class Marvel:
    def __init__(self, dev_keys_file):
        self.dev_keys_json = self._load_dev_keys_json(dev_keys_file)
        self.endpoint = 'http://gateway.marvel.com/v1/public/'

    def _load_dev_keys_json(self, dev_keys_file):
        """
        Load Marvel API Developer keys from a 'key=value' file
        Expects file contents in the following format,
        recommended to be kept in a local encrypted folder (encfs):
        public=<your key>
        private=<your key>

        :param dev_keys_file: File path to a keys file
        :return: JSON containing a private/public key pair
        """
        dev_keys_path = path.expanduser(dev_keys_file)
        print('Reading dev keys from {}'.format(dev_keys_path))
        dev_keys = {'public': None, 'private': None}
        try:
            with open(dev_keys_path, 'r') as dkf:
                lines = dkf.readlines()
        except IOError as e:
            raise Exception('Keys file {} not found: '.format(dev_keys_path, e))
        for line in lines:
            line = line.strip()
            for dev_key in dev_keys.keys():
                if line.startswith(dev_key):
                    dev_keys[dev_key] = line.split('=', 1)[1]
        return dev_keys

    def _auth(self):
        """
        Creates hash from API keys and returns all required parameters
        Adapted from https://github.com/gpennington/PyMarvel/blob/master/marvel/marvel.py#L69

        :return: str -- URL encoded query parameters containing 'ts', 'apikey', and 'hash'
        """
        public = self.dev_keys_json['public']
        private = self.dev_keys_json['private']

        ts = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        # UTF-8 encoding must take place at the point of hashing:
        # https://stackoverflow.com/a/31477467/3900915
        hash_string = md5('{}{}{}'.format(ts, private, public).encode('utf-8')).hexdigest()
        return 'ts={}&apikey={}&hash={}'.format(ts, public, hash_string)

    def bifrost(self, resource_url):
        """
        Calls the Marvel API endpoint
        Adapated from https://github.com/gpennington/PyMarvel/blob/master/marvel/marvel.py#L38

        :param resource_url: URL Slug of the resource
        :return: Requests response
        """
        # TODO: add parameter support
        url = '{}{}?{}'.format(self.endpoint, resource_url, self._auth())
        # print(url)
        return requests.get(url)


def main():
    a_test = Marvel(dev_keys_file='~/visible_sec/marvel_dev.keys')
    # print('Public Key: {}'.format(a_test.dev_keys_json['public']))
    # print('Private Key: {}'.format(a_test.dev_keys_json['private']))

    # Get Comic Characters?
    test_result = a_test.bifrost(resource_url='characters')
    print('REQUEST URL: {}'.format(test_result.url))
    print(dumps(test_result.json(), indent=2))
    # print('CONTENT: {}'.format(test_result.content))
    # print('HEADERS: {}'.format(test_result.headers))
    # print('HISTORY: {}'.format(test_result.history))
    # print('LINKS: {}'.format(test_result.links))
    # print('REQUEST: {}'.format(test_result.request))


if __name__ == '__main__':
    main()