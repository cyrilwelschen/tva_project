'__author__' == 'cyril'


class Factor(object):
    """
    Class describing factors (value or cost)
    """

    def __init__(self, name, value=None, error=None, description=None,
                 interval=None, subvalues=None, subvalue_formula=None,
                 **kwargs):
        """
        Initialise data struct.
        :param value: cost or value (usually numerical)
        :param error: corresponding error
        :param args: list of additional values
        :param kwargs: dictionary of additional information
        """
        self.name = name
        if value and subvalues:
            print("WARNING: Shouldn't set both value and subvalues!!")
        self.val = value
        self.err = error
        self.subs = subvalues
        self.sub_func = subvalue_formula
        self.des = description
        self.inter = interval
        self.factor_kwargs = kwargs
        self.tech = kwargs.get('technology', None)
        self.var_type = kwargs.get('var_type', type(self.val))
        self.unit = kwargs.get('unit', None)

    def info(self):
        return vars(self)

    @property
    def error_type(self):
        return type(self.err)
