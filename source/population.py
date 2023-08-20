import numpy as np
from agent import Agent
import random

class Population:
    def __init__(self):
        pass
    
    
    def sample_population(
                          population_size:int,
                          lambda_family_size:int,
                          lambda_acquaintance_size:int,
                          scalar_factors_distribution):
        """
        Returns a list of "Agent" objects.
        
        The number of family members each family has follows Poisson distribution.
        
        The number of acquaintances each person has follows Poisson distribution.
        
        scalar_factors_distribution specifies what scalar_factors values are possible and what their frequencies in the population are, for example:
        
            scalar_factors_distribution = {
                "age_group": {
                    "values": ["children", "adolescent", "adult"],
                    "weights": [0.25,0.25,0.5]
                },
                "sex":{
                    "values": ["male", "female"],
                    "weights": [0.47, 0.53]
                }
            }

        """
        
        
        agents = []
        for index in range(population_size):
            agents.append(Agent(index))
            
        # scalar_factors sampling
        for scalar_factor in scalar_factors_distribution:
            for agent in agents:
                agent.scalar_factors[scalar_factor] = None
                agent.scalar_factors[scalar_factor] = random.choices(
                    scalar_factors_distribution[scalar_factor]["values"],
                    scalar_factors_distribution[scalar_factor]["weights"]
                )[0]
        
        # Household 
        random_list = list(range(population_size))
        np.random.shuffle(random_list)
        left = 0
        family_index = 0
        count = 0
        while left < population_size:
            
            right = left + 1 + np.random.poisson(lam=lambda_family_size)
            if right >= population_size:
                right = population_size
            family_member_indices = random_list[left:right]
            for family_member_index in family_member_indices:
                # Attribute: family_members
                agents[family_member_index].family_members = family_member_indices.copy()
                agents[family_member_index].family_members.remove(family_member_index)
                
                possible_acquaintances = random_list[:left] + random_list[right:]
                num_of_acquaintances = np.random.poisson(lam=lambda_acquaintance_size)
                acquaintances = random.sample(possible_acquaintances, num_of_acquaintances)
                agents[family_member_index].acquaintances = acquaintances
                
            left = right
        
        return agents

