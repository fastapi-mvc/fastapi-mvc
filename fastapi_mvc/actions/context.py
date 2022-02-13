""""""


class Context(object):

    def __init__(self, action):
        self._action = action

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    def execute(self, *args, **kwargs):
        self._action.execute(*args, **kwargs)
