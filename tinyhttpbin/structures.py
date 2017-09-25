# -*- coding: utf-8 -*-


class CaseInsensitiveDict(dict):
    def _lower_keys(self):
        return [k.lower() for k in self.keys()]

    def __contains__(self, key):
        return key.lower() in self._lower_keys()

    def __getitem__(self, key):
        if key in self:
            return list(self.items())[self._lower_keys().index(key.lower())][1]