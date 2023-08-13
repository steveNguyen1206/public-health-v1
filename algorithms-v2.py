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
    def __init__(self, id, scalar_factors=None):
        self.id = id
        self.family_members = []
        self.acquaintances = []
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
        '''
        If agent is still in infection period, decrease their infection time by 1 unit. If agent has finished their infection period, use a fatality rate generator to determine if they will die or not.
        If agent is still INCUBATED, decrease their incubation time by 1 unit. If agent has finished their incubation period, they will be moved to INFECTED status. 
        '''
        
        if self.status == INFECTED and self.infection_days_left > 0:
            self.infection_days_left -= 1
        
        if self.status == INFECTED and self.infection_days_left <= 0:
            if fatality_rate_generator() == True:
                self.status = DECEASED
            else:
                self.status = RECOVERED
            
            
        if self.status == INCUBATED:
            self.incubation_days_left -= 1
            if self.incubation_days_left <= 0:
                self.start_infection(infection_period_generator)


class EdgeSampler:
    def __init__(self,
                 agents: list[Agent],
                 non_hh_contact_matrix,
                 ):
        self.contact_matrix = non_hh_contact_matrix
        self.hh_dict = {}
        self.non_hh_dict = {}
        self.scalar_factor = self.contact_matrix["scalar_factor"]
        self.factor_array = [0] * len(agents)
        
        for index, agent in enumerate(agents):
            self.factor_array[index] = agent.scalar_factors[self.scalar_factor]
        
        
        for index, agent in enumerate(agents):    
            self.hh_dict[index] = agent.family_members
            self.non_hh_dict[index] = {}
            for acquaintance_index in agent.acquaintances:
                acquaintance_factor = self.factor_array[acquaintance_index]
                self.non_hh_dict[index][acquaintance_factor].append(acquaintance_index)


    def sample_edges(self):
        edge = {}
        for index in self.hh_dict:
            edge[index]["family_members"] = self.hh_dict[index]
        for index in self.non_hh_dict:
            for target_factor_value in self.non_hh_dict[index]:
                n_of_contacts = np.random.poisson(self.contact_matrix["values"]
                                                [self.scalar_factor[index]]
                                                [target_factor_value]
                                                )
                if n_of_contacts > len(self.non_hh_dict[index][target_factor_value]):
                    n_of_contacts = len(self.non_hh_dict[index][target_factor_value])
                    
            edge[index]["acquaintances"].extend(random.sample(self.non_hh_dict[index][target_factor_value],
                                                              n_of_contacts))
        return edge


class WeightSampler:
    def __init__(self,
                 weight_dist):
        self.weight_dist = weight_dist

    def sample_weights(self, edge):
        weight = {}
        for index in edge:
            weight[index] = {}
            for connection_type in edge[index]:
                for target in edge[index][connection_type]:
                    weight[index][target] = random.choices(self.weight_dist[connection_type]["risk_ratio"],
                                                           self.weight_dist[connection_type]["weight"])[0]
        return weight


class DiseaseSimulation:
    def __init__(self,
                 agents: list[Agent],
                 n_days: int,
                 edge_sampler: EdgeSampler,
                 weight_sampler: WeightSampler,
                 incubation_period_generator,
                 infection_period_generator,
                 fatality_rate_generator,
                 ):
        self.result_df = None
        self.agents = agents
        self.n_days = n_days
        self.incubation_period_generator = incubation_period_generator
        self.infection_period_generator = infection_period_generator
        self.fatality_rate_generator = fatality_rate_generator
    
    
    def run_simulation(self):
        daily_result = []
        for day in self.n_days:
            edge = EdgeSampler.sample_edges()
            weight = WeightSampler.sample_weights(edge=edge)
            
        
        
        return daily_result[]
        
        
        

        
        

