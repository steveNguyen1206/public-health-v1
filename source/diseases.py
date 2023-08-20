from scipy.stats import lognorm, bernoulli
import numpy as np

class Disease:
    def __init__(self):
        pass
    


class Ebola(Disease):
    def __init__(self):
        self.pr_base = 0.01962 
    
    
    def generate_incubation_period(self):
        return lognorm.rvs(s=0.284, scale=np.exp(2.446))
    
    
    def generate_infection_period(self):
        return lognorm.rvs(s=0.1332, scale=np.exp(2.2915))
    
    
    def generate_fatality(self):
        return bernoulli.rvs(0.85)
    
