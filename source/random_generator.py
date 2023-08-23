import numpy as np
import random
from scipy.stats import  lognorm


class RandomGenerator:
    class Generator:
        def __init__(self, *args):
            self.parameters = args
        
        # abstract method
        def generate_random_values(self, *args):
            pass


    class PoissonRandomGenerator(Generator):
        def __init__(self, lam):
            super().__init__(lam)
            self.lam = lam
        
        
        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return np.random.poisson(self.lam, size=size)
        
        
    class NormalRandomGenerator(Generator):
        def __init__(self, mu=0.0, sigma=1.0):
            super().__init__(mu, sigma)
            self.mu = mu
            self.sigma = sigma
            
            
        def generate_random_values(self, size=1):
            if size < 1:
                size = 1
            return np.random.normal(loc=self.mu, scale=self.sigma**2, size=size)


    class LogNormalRandomGenerator(Generator):
        def __init__(self, mu=0.0, sigma=1.0):
            super().__init__(mu, sigma)
            self.mu = mu
            self.sigma = sigma
            
        
        def generate_random_values(self, *args):
            if size < 1:
                size = 1
            return np.random.log(loc=self.mu, scale=self.sigma**2, size=size)
        
        
    class BernoulliRandomGenerator(Generator):
        def __init__(self, probability=0.5):
            super().__init__(probability)
            self.probability = probability
            
        
        def generate_random_values(self, size):
            if size < 1:
                size = 1
            return scipy.stats.bernoulli(self.probability,size=size)
        
        
    class  BinomialRandomGenerator(Generator):
        def __init__(self, p, n):
            super().__init__(p, n)
            self.p = p
            self.n = n
            
        
        def generate_random_values(self, size):
            if size < 1:
                size = 1
            return np.random.binomial(self.n,self.p,size)
        
        

        