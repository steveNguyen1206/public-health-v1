import random 
import numpy as np
import json
import  pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import lognorm, bernoulli
from itertools import combinations

SUSCEPTIBLE = 0
INCUBATED = 1
INFECTED = 2
VACCINATED = 3
REMOVED = 4
RECOVERED = 4
IMMUNE = 4
DECEASED = 5

class Agent:
    def __init__(self, index, family=None, scalar_factors=None):
        self.index = index
        self.family = family
        self.status = SUSCEPTIBLE
        self.incubation_days_left = 0 
        self.infection_days_left = 0
        if scalar_factors is None:
            self.scalar_factors = {}
        self.scalar_factors = scalar_factors
        
    
    def start_incubation(self, incubation_period_generator):
        '''
        Start an agent's incubation period, with the period time given by a generator function.
        The period generator function wraps around a random function that generates a scalar value.
        
        '''
        self.status = INCUBATED
        self.incubation_days_left = incubation_period_generator()
    
    
    def start_infection(self, infection_period_generator):
        '''
        Start an agent's infection period, with the period time given by a generator function.
        The period generator function wraps around a random function that generates a scalar value.
        '''
        self.status = INFECTED
        self.infection_days_left = infection_period_generator()
    
        
    def update_status(self, 
                      infection_period_generator,
                      fatality_rate_generator
    ): 
        if self.status == SUSCEPTIBLE:
            self.incubation_days_left -= 1
            if self.incubation_days_left <= 0:
                self.start_infection(infection_period_generator)
        else
        if self.status == INFECTED:
            
        
                