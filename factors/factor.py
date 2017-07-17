'__author__' == 'cyril'


class Factor(object):
    """
    Class describing factors (value or cost)
    """

    def __init__(self, value, error=None, args=None, kwargs=None):
        """
        Initialise data struct.
        :param value: cost or value (usually numerical)
        :param error: corresponding error
        :param args: list of additional values
        :param kwargs: dictionary of additional information
        """
        self.val = value
        self.err = error
        self.args = args
        self.kwargs = kwargs
        self.var_name = kwargs.get('variable_name', None)

    @property
    def value_type(self):
        return type(self.val)

    @property
    def error_type(self):
        return type(self.err)
