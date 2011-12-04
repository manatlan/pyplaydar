class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, '_list'):
            cls._list = []
        else:
            cls._list.append(cls)

    @property
    def list(self):
        return Resolver._list

class Resolver:
    __metaclass__ = PluginMount
