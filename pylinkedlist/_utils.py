def mutates_length(always=False, decrements=False):
    """Decorator to indicate that execution of a method will change the length

    :param bool always: Specifies whether the decorate method always changes the
    length or not. In other words, the change in length is not dependent on what
    the method returns.
    :param bool decrements: By default, the decorator will increase the length unless
    this parameter is set to ``True``.
    """
    def wrapper(method):
        def incrementer(self, *args, **kwargs):
            method_output = method(self, *args, **kwargs)
            if always or (not always and method_output):
                if (method_output is None) or (method_output is True):
                    scalar = 1
                elif isinstance(method_output, int):
                    scalar = method_output
                else:
                    message = 'method ({}()) returned unexpected value "{}"'.format(
                        method.__name__, method_output)
                    assert False, message
                self._length += scalar if not decrements else -scalar
            return method_output
        return incrementer
    return wrapper
    