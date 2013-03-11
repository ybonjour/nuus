__author__ = 'Yves Bonjour'

class Mock(object):
    def __init__(self):
        self.method_calls = {}

    def num_method_calls(self, method):
            return len(self.get_calls(method))

    def get_calls(self, method):
        return self.method_calls.get(method, [])

    def get_arguments(self, method, call_number=1):
        method_calls = self.get_calls(method)
        if call_number > len(method_calls) or call_number < 1:
            raise RuntimeError("call_number out of range, method was not called often enough")

        return method_calls[call_number-1]

    def was_called(self, method):
        return method in self.method_calls

    def _handle_method_call(self, method, arguments=None):
        if method not in self.method_calls:
            self.method_calls[method] = []
        self.method_calls[method].append(arguments)

    def __getattr__(self, name):
        def method(*args):
            method_args = tuple(args) if args else None
            self._handle_method_call(name, tuple(method_args))
        return method