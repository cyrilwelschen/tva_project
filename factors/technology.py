'__author__' == 'cyril'


from tva_project.factors.factor import Factor


class Technology(object):

    def __init__(self, name, models=None, factors=None):
        self.name = name
        self.models = [] if models is None else models
        self.factors = [] if factors is None else factors

    def add_model(self, model):
        self.models.append(model)

    def add_fac(self, fac):
        if isinstance(fac, Factor):
            self.factors.append(fac)
        else:
            print("Can only add instances of type 'Factor'")

    def get_factors(self):
        return self.factors

    def factor_names(self):
        return [f.name for f in self.factors]

    def model(self, timesteps=None):
        details = self.model_details(timesteps)
        model_sum = [0]
        for d in details:
            summ = 0
            for f in d.values():
                summ += f
            model_sum.append(summ)
        return range(1, timesteps+1), model_sum, details

    def model_details(self, timesteps):
        steps = []
        t = 1
        while t < timesteps:
            factorlist = {}
            for f in self.get_factors():
                factorlist[f.name] = f.val * int(t % f.inter == 0)
            """
            factorlist["current_step"] = t
            factorlist["timeline"] = timesteps
            factorlist["taken factors"] = self.get_factors()
            """
            steps.append(factorlist)
            t += 1
