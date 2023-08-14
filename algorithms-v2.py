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
        self.vaccination_wait_days_left = 0
        if scalar_factors is None:
            self.scalar_factors = {}
        else:
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
                
                
        if self.status == VACCINATED:
            if self.vaccination_wait_days_left <= 0:
                self.status = IMMUNE
            else:
                self.vaccination_wait_days_left -= 1


class EdgeSampler:
    def __init__(self,
                 agents: list[Agent],
                 non_hh_contact_matrix,
                 ):
        # contact_matrix = {
        #     "scalar_factor": "age_group",
        #     "values": {
        #         "children": {"children": 0.2, 
        #                      "adolescent": 0.6, 
        #                      "adult": 0.4},
        #         "adolescent": {"children": 0.6,
        #                        "adolescent": 0.5,
        #                        "adult": 0.1},
        #         "adult": {"children": 0.4,
        #                   "adolescent": 0.1,
        #                   "adult": 0.3}
        #     }
        # }
        
        
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
                 pr_base
                 ):
        self.result_df = None
        self.agents = agents
        self.n_days = n_days
        self.incubation_period_generator = incubation_period_generator
        self.infection_period_generator = infection_period_generator
        self.fatality_rate_generator = fatality_rate_generator
        self.pr_base = pr_base
    
    
    def run_simulation(self):
        res = pd.DataFrame({"day": [],
                        "susceptible": [],
                        "incubated": [],
                        "infected": [],
                        "dead": [],
                        "vaccinated": [],
                        "removed": []})
        res.set_index("day", inplace=True)
    
        for day in self.n_days:
            # Establish edges and weights
            edge = EdgeSampler.sample_edges()
            weight = WeightSampler.sample_weights(edge=edge)
            
            # Iterate through all agents in the system
            for agent_index, agent in enumerate(self.agents):
                if agent.status == INFECTED and agent.infection_days_left > 0:
                    for contact_type in edge[agent_index]:
                        for contact_index in edge[agent_index][contact_type]:
                            contact = agent[contact_index]
                            prob = self.pr_base * weight[agent_index][contact_index]
                            if bernoulli.rvs(prob) == 1:
                                agent.start_incubation(self.incubation_period_generator)
                
                agent.update_status(self.infection_period_generator,
                                    self.fatalilty_rate_generator)
            
        
            status_count = [0, 0, 0, 0, 0, 0]
            # Count the number of agents having the same status.
            for agent in self.agents:
                status_count[agent.status] += 1
                
        
            today = pd.DataFrame([{"day": day,
                                "susceptible": status_count[SUSCEPTIBLE],
                                "incubated": status_count[INCUBATED],
                                "infected": status_count[INFECTED],
                                    "vaccinated": status_count[VACCINATED],
                                "removed": status_count[REMOVED],
                                "deceased": status_count[DECEASED],

                                }]) 
            res = pd.concat([res, today],ignore_index=True)
            

        return res


class Ebola:
    def __init__(self):
        pass
    
    
    def generate_incubation_period():
        return lognorm.rvs(s=0.284, scale=np.exp(2.446))
    
    
    def generate_infection_period():
        return lognorm.rvs(s=0.1332, scale=np.exp(2.2915))
    
    
    def generate_fatality_rate():
        return bernoulli(0.85)
    

class Population:
    def __init__(self,
                 N,
                 family_size,
                 acquantaince_size,
                 scalar_factors_distribution):
        self.n_population = N
        self.family_size = family_size
        self.acquaintance_size = acquantaince_size
        self.scalar_factors_distribution = scalar_factors_distribution
        
    
    
    def population_sample(self):
        agents = []
        for index in range(self.n_population):
            agents.append(Agent(index))
            
        # scalar_factors sampling
        for scalar_factor in self.scalar_factors_distribution:
            for agent in agents:
                agent.scalar_factors[scalar_factor] = None
                agent.scalar_factors[scalar_factor] = random.choices(
                    self.scalar_factors_distribution[scalar_factor]["values"],
                    self.scalar_factors_distribution[scalar_factor]["weights"]
                )        
        
        # Household 
        hh_dict = {}
        random_list = list(range(self.n_population))
        np.random.shuffle(random_list)
        left = 0
        family_index = 0
        while left < self.n_population:
            right = left + 1 + np.random.poisson(lam=self.family_size)
            if right >= self.n_population:
                right = self.n_population
            family_member_indices = random_list[left:right]
            
            
            for family_member_index in family_member_indices:
                # Attribute: family_members
                agents[family_member_index].family_members = family_member_indices
                agents[family_member_index].family_members.remove(family_member_index)

                
                possible_acquaintances = random_list[:left] + random_list[right:]
                num_of_acquaintances = np.random.poisson(lam=self.acquaintance_size)
                acquaintances = random.sample(possible_acquaintances, num_of_acquaintances)
                agents[family_member_index].acquaintances = acquaintances
                
            left = right + 1
            family_index = family_index + 1
        
        return agents



scalar_factors_distribution = {
    "age_group": {
        "values": ["children", "adolescent", "adult"],
        "weights": [0.33,0.33,0.33]
    }
}


pop = Population(100, 4, 10,scalar_factors_distribution=scalar_factors_distribution)
agents = pop.population_sample()
for agent in agents:
    print(