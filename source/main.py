import random 
import numpy as np
import json
import  pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import lognorm, bernoulli
from itertools import combinations
import time

SUSCEPTIBLE = 0
INCUBATED = 1
INFECTED = 2
VACCINATED = 3
REMOVED = 4
RECOVERED = 4
IMMUNE = 4
DECEASED = 5

from agent import Agent
from diseases import Ebola
from vaccine import Vaccine
from contact import EdgeSampler, WeightSampler
from population import Population
from disease_simulation import DiseaseSimulation

scalar_factors_distribution = {
    "age_group": {
        "values": ["children", "adolescent", "adult"],
        "weights": [0.25,0.25,0.5]
    }
}
contact_matrix = {
            "scalar_factor": "age_group",
            "values": {
                "children": {"children": 0.2, 
                             "adolescent": 2.0, 
                             "adult": 1.2},
                "adolescent": {"children": 2.0,
                               "adolescent": 3.6,
                               "adult": 1.5},
                "adult": {"children": 1.2,
                          "adolescent": 1.5,
                          "adult": 5.3}
            }
        }
weight_dist = {
    "family_members": {
        "weights": [0.163, 
                       0.403, 
                       0.17, 
                       0.026, 
                       0.1, 
                       0.138],
        "values": [9.7, 
                       8.3,
                       5.6,
                       4.9,
                       1.3,
                       1
                       ]
    },
    "acquaintances": {
        "weights": [1],
        "values": [2.45],
    },  
}
n_pop = 700

agents = Population.sample_population(n_pop, 
                                      4, 10, 
                                      scalar_factors_distribution)


edge_sampler = EdgeSampler(agents,non_hh_contact_matrix=contact_matrix)
weight_sampler = WeightSampler(weight_dist)
vaccine = Vaccine(num_vaccine=5, effciency=0.998, reach_rate=0.7, immune_period=9)
ebola = Ebola()
simulation = DiseaseSimulation(agents,
                               100,
                               edge_sampler,
                               weight_sampler,
                               ebola,
                               vaccine)
simulation.initialize_seed_cases(15)



start_time = time.time() #------------------------
res = simulation.run_simulation() 
end_time = time.time() #--------------------------

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")


plot = res[['susceptible', 'incubated', 'infected', 'deceased', 'removed']].div(n_pop).plot()
plot.set_xlabel("Day")
plot.set_ylabel("Ratio of population")
plot.set_title('Simulation')
plot.set_xticks(range(0, len(res), 20))
plt.show()




# class Simulation:
#     def __init__(self):
#         self.agents = []
#         self.parameters = {}
        
    
#     def init_population(self, df_pop, json_household):
#         # Agent initialization, household included
#         for index, row in df_pop.iterrows():
#             # Two scalar factors: age and sex
#             factors = {"age": row['age'],
#                        "sex": row['sex']}
            
#             # Initializes with id and scalar_factors
#             new_agent = Agent(id=row['id'],
#                               scalar_factors=factors)
            
#             # Adds members of their respective family
#             new_agent.family_members = json_household[row['family_id']].copy().remove(new_agent.id)
#             self.agents.append(new_agent)
        

#     def init_parameters(self, json_parameters):
#         self.parameters = json_parameters
        
        
#     def init_acquaintances(self):
#         n_pop = len(self.agents)
#         random_list = list(range(n_pop))
#         for agent in self.agents:
#             n_acquaintances = np.random.poisson(lam=10)
#             possible_acquaintance_indices = random.sample(random_list, n_acquaintances)
#             for possible_acquaintance_index in possible_acquaintance_indices:
#                 possible_acquaintance_id = self.agents[possible_acquaintance_index].id
#                 if possible_acquaintance_id != agent.id and possible_acquaintance_id not in agent.family_members:
#                     agent.acquaintances.append(possible_acquaintance_id)
    

#     def run():
#         pass    
    
    
    
    
    