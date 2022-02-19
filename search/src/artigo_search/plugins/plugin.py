from artigo_search.utils import convert_name


class Plugin:
    default_config = {}
    default_version = '0.1'

    def __init__(self, config=None, name=None):
        self._config = self.default_config

        if config is not None:
            self._config.update(config)

        self._version = self.default_version

        if name is None:
            name = convert_name(self.__class__.__name__)

        self._name = name

    @property
    def config(self):
        return self._config

    @property
    def version(self):
        return self._version

    @property
    def name(self):
        return self._name
