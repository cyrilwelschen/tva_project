'__author__' == 'cyril'


class Model(object):
    """
    Class describing modelling of total SC revenue over time
    """

    def __init__(self, value, error=None, args=None, kwargs=None):
        """
        Initialise model properties
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

