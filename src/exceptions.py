class UnsuccessfulAuthError(Exception):
    pass


class UnsuccessfulTokenRefreshError(Exception):
    pass


class LocalStorageItemIsNotFoundError(Exception):

    def __init__(self, *args, key: str):
        super().__init__(*args)
        self.key = key
