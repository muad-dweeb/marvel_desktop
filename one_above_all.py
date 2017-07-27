from os import path


class Marvel:
    def __init__(self, dev_keys_file):
        self.dev_keys_json = self.load_dev_keys_json(dev_keys_file)

    def load_dev_keys_json(self, dev_keys_file):
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


def main():
    a_test = Marvel(dev_keys_file='~/visible_sec/marvel_dev.keys')
    print('Public Key: {}'.format(a_test.dev_keys_json['public']))
    print('Private Key: {}'.format(a_test.dev_keys_json['private']))


if __name__ == '__main__':
    main()