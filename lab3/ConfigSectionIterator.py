class ConfigSectionIterator:
    def __init__(self, config: dict):
        self._sections = list(config.items())
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._sections):
            raise StopIteration
        section = self._sections[self._index]
        self._index += 1
        return section