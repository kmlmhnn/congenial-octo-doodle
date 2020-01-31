from collections import OrderedDict


class CacheError(Exception):
    pass


class CacheInitializationError(CacheError):
    pass


class LRUCache:
    def __init__(self, nmemb):
        if not isinstance(nmemb, int):
            raise CacheInitializationError("nmemb cannot be a non-integer")
        if nmemb < 1:
            raise CacheInitializationError("nmemb must be greater than or equal to 1")
        self.nmemb = nmemb
        self.members = OrderedDict()

    def __getitem__(self, key):
        self.members.move_to_end(key)
        return self.members[key]

    def __setitem__(self, key, value):
        if not len(self.members) < self.nmemb:
            self.members.popitem(last=False)
        self.members[key] = value
        self.members.move_to_end(key)
