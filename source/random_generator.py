import numpy as np
import random
from scipy.stats import *


class RandomGenerator:
    def __init__(self):
        pass

    def create_from_json(self,data:dict):
        random_type = data.get("type")
        properties = data.get("properties")
        match random_type:
            case "random_Poisson": return self.PoissonRandomGenerator(json_data=properties)
            case "random_normal": return self.NormalRandomGenerator(json_data=properties)
            case "random_log-normal": return self.LogNormalRandomGenerator(json_data=properties)
            case "random_bernoulli": return self.BernoulliRandomGenerator(json_data=properties)
            case "random_binomial": return self.BinomialRandomGenerator(json_data=properties)      
    
    
    class Generator:
        def __init__(self, *args, json_data=None):
            pass
            
        
        # abstract methods
        def generate_random_values(self, *args):
            pass
        

    class PoissonRandomGenerator(Generator):
        def __init__(self, lam=0, json_data=None):
            super().__init__(lam, json_data)
            if json_data is not None:
                self.lam = json_data.get("lambda")
            else:
                self.lam = lam
                

        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return np.random.poisson(self.lam, size=size)
        
        
    class NormalRandomGenerator(Generator):
        def __init__(self, mu=0.0, sigma=1.0, json_data=None):
            super().__init__(mu, sigma,json_data)
            if json_data is None:
                self.mu = mu
                self.sigma = sigma
            else:
                self.mu = json_data.get("mu")
                self.sigma = json_data.get("sigma") 
            
            
        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return np.random.normal(loc=self.mu, scale=self.sigma**2, size=size)


    class LogNormalRandomGenerator(Generator):
        def __init__(self, mu=0.0, sigma=1.0, json_data = None):
            super().__init__(mu, sigma,json_data)
            if json_data is None:
                self.mu = mu
                self.sigma = sigma
            else:
                self.mu = json_data.get("mu")
                self.sigma = json_data.get("sigma") 
            
        
        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return np.random.log(loc=self.mu, scale=self.sigma**2, size=size)
        
        
    class BernoulliRandomGenerator(Generator):
        def __init__(self, probability=0.5, json_data=None):
            super().__init__(probability, json_data)
            if json_data is None:
                self.probability = probability
            else:
                self.probability = json_data.get("probability")

        
        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return bernoulli.rvs(self.probability,size=size)
        
        
    class  BinomialRandomGenerator(Generator):
        def __init__(self, p, n, json_data=None):
            super().__init__(p, n, json_data)
            if json_data is None:
                self.p = p
                self.n = n
            else:
                self.p = json_data.get("p")
                self.n = json_data.get("n")
            
        
        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return np.random.binomial(self.n,self.p,size)
        
rand = RandomGenerator()
gen = rand.create_from_json(data={"type": "random_Poisson", "properties": {"lambda":6}})
print([gen.generate_random_values()[0] for _ in range(10)])