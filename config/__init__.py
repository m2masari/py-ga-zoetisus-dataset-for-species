import os


class Options:
    def __init__(self):
        self._version = "1.0.0"
        self._version_timestamp = "1588595298"
        self._dir_config = "config"
        self._dir_temp = "_temp"
        self._dir_log = "_logs"
        self._dir_export = "_exports"
        self._dir_request = "_requests"
        self._dir_response = "_responses"
        self._client_secrets = "client_secrets.json"
        self._ga_accounts = "accounts.csv"

    @property
    def version(self):
        return self._version

    @property
    def version_timestamp(self):
        return self._version_timestamp

    @property
    def dir_temp(self):
        return os.path.join(os.getcwd(), self._dir_temp)

    @property
    def dir_log(self):
        return os.path.join(os.getcwd(), self._dir_log)

    @property
    def dir_export(self):
        return os.path.join(os.getcwd(), self._dir_export)

    @property
    def dir_request(self):
        return os.path.join(os.getcwd(), self._dir_request)

    @property
    def dir_response(self):
        return os.path.join(os.getcwd(), self._dir_response)

    @property
    def client_secrets(self):
        return os.path.join(os.getcwd(), self._dir_config, self._client_secrets)

    @property
    def ga_accounts(self):
        return os.path.join(os.getcwd(), self._dir_config, self._ga_accounts)


options = Options()

folders = [options.dir_temp, options.dir_log, options.dir_export, options.dir_request, options.dir_response]

for folder in folders:
    if not os.path.exists(folder):
        try:
            os.mkdir(folder)
        except OSError as error:
            print(error)

