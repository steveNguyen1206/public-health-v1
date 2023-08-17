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
        
    
    def start_incubation(self, incubation_period):
        '''
        Start an agent's incubation period, with the period time given by a generator function.
        The period generator function wraps around a random function that generates a scalar value.
        
        '''
        self.status = INCUBATED
        self.incubation_days_left = incubation_period

    
    def start_infection(self, infection_period):
        '''
        Start an agent's infection period, with the period time given by a generator function.
        The period generator function wraps around a random function that generates a scalar value.
        '''
        self.status = INFECTED
        self.infection_days_left = infection_period
    
        
    def update_status(self, 
                      infection_period,
                      fatality
    ): 
        '''
        If agent is still INCUBATED, decrease their incubation time by 1 unit. If agent has finished their incubation period, they will be moved to INFECTED status. 
        '''
        
        if self.status == INFECTED and self.infection_days_left <= 0:
            if fatality == True:
                self.status = DECEASED
            else:
                self.status = RECOVERED
            
            
        elif self.status == INCUBATED:
            self.incubation_days_left -= 1
            if self.incubation_days_left <= 0:
                self.start_infection(infection_period)
                
                
        elif self.status == VACCINATED:
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
                if acquaintance_factor not in self.non_hh_dict[index]:
                    self.non_hh_dict[index][acquaintance_factor] = list()
                self.non_hh_dict[index][acquaintance_factor].append(acquaintance_index)


    def sample_edges(self):
        edge = {}
        for index in self.hh_dict:
            edge[index] = {}
            edge[index]["family_members"] = self.hh_dict[index]
        for index in self.non_hh_dict:
            edge[index]["acquaintances"] = list()
            
            for target_factor_value in self.non_hh_dict[index]:
                n_of_contacts = np.random.poisson(self.contact_matrix["values"][self.factor_array[index]][target_factor_value])
                if n_of_contacts > len(self.non_hh_dict[index][target_factor_value]):
                    n_of_contacts = len(self.non_hh_dict[index][target_factor_value])
                    
                edge[index]["acquaintances"].extend(random.sample(self.non_hh_dict[index][target_factor_value], n_of_contacts))
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
                    weight[index][target] = random.choices(self.weight_dist[connection_type]["values"],
                                                           self.weight_dist[connection_type]["weights"])[0]
        return weight


class DiseaseSimulation:
    def __init__(self,
                 agents: list[Agent],
                 n_days: int,
                 edge_sampler: EdgeSampler,
                 weight_sampler: WeightSampler,
                 disease,
                 vaccine
                 ):
        self.result_df = None
        self.agents = agents
        self.n_days = n_days
        self.disease = disease
        self.edge_sampler = edge_sampler
        self.weight_sampler = weight_sampler
        self.vaccine = vaccine
    
    
    def initialize_seed_cases(self, n_seed_cases):
        seed_indices  = random.sample(list(range(0, len(self.agents))), n_seed_cases)
        # Update seed cases
        for seed_index in seed_indices:
            self.agents[seed_index].start_infection(self.disease.generate_infection_period())
    
    
    def run_simulation(self):
        res = pd.DataFrame({"day": [],
                        "susceptible": [],
                        "incubated": [],
                        "infected": [],
                        "vaccinated": [],
                        "removed": [],
                        "deceased": [],})
        res.set_index("day", inplace=True)

        for day in range(self.n_days):
            # Establish edges and weights
            edge = self.edge_sampler.sample_edges()
            weight = self.weight_sampler.sample_weights(edge=edge)
            daily_infected=[]
            # Iterate through all agents in the system
            for agent_index, agent in enumerate(self.agents):
                # If this agent is still infectious
                if agent.status == INFECTED and agent.infection_days_left > 0:
                    # iterate through their contacts
                    for contact_type in edge[agent_index]:
                        for contact_index in edge[agent_index][contact_type]:
                            contact = agents[contact_index]
                            if contact.status == SUSCEPTIBLE:
                                prob = self.disease.pr_base * weight[agent_index][contact_index]
                                if bernoulli.rvs(prob) == 1:
                                    contact.start_incubation(self.disease.generate_incubation_period())
                        
                            for sub_contact_type in edge[contact_index]:
                                for sub_contact_index in edge[contact_index][sub_contact_type]:
                                    sub_prob = self.disease.pr_base * self.disease.pr_base * weight[agent_index][contact_index] * weight[contact_index][sub_contact_index]
                                    if agents[sub_contact_index].status in [SUSCEPTIBLE]:
                                        if agents[contact_index].status == INFECTED:
                                            sub_prob = weight[contact_index][sub_contact_index] * self.disease.pr_base
                                        else:
                                            sub_prob = self.disease.pr_base * self.disease.pr_base * weight[agent_index][contact_index] * weight[contact_index][sub_contact_index]
                                        if sub_prob > 1:
                                            sub_prob = 1
                                        if (bernoulli.rvs(sub_prob) == 1):
                                            agents[sub_contact_index].start_incubation(self.disease.generate_incubation_period())    
                    
                    
                    agent.infection_days_left -= 1
                    daily_infected.append(agent)
                else:
                    agent.update_status(self.disease.generate_infection_period(),
                                        self.disease.generate_fatality())
            
            self.ring_based_vaccination(edge,weight,daily_infected)
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
    
    def ring_based_vaccination(self,edge,weight,daily_infected):
        contacts=[]
        contacts_of_contacts=[]
        risk={}
        for  agent in daily_infected:
            for contact_type in edge[agent.id]:
                for contact_index in edge[agent.id][contact_type]:
                    contact = agents[contact_index]
                    if contact.status == SUSCEPTIBLE:
                        prob = self.disease.pr_base * weight[agent.id][contact_index]
                        risk[contact_index]=prob
                        contacts.append(contact)

        for  c in contacts:
            for cc_type in edge[c.id]:
                for cc_index in edge[c.id][cc_type]:
                    cc = agents[cc_index]
                    contacts_of_contacts.append(cc)
                    if cc.status == SUSCEPTIBLE:
                        prob = self.disease.pr_base * weight[c.id][cc_index] * risk[c.id]
                        risk[cc_index]=prob
        risk_sorted = dict(sorted(risk.items(), key=lambda item: item[1]))
        vax_used = 0
        for i in risk_sorted:
            if vax_used < self.vaccine.num_vaccine:
                if bernoulli.rvs(self.vaccine.reach_rate, 1 - self.vaccine.reach_rate) == 1:
                    # print(self.agents[i].id)
                    if self.agents[i].status == INCUBATED:
                        if bernoulli.rvs(self.effciency, 1 - self.vaccine.effciency) == 1:
                            self.agents[i].status = VACCINATED
                            self.agents[i].vaccination_wait_days_left= self.vaccine.immune_period
                    elif self.agents[i].status == SUSCEPTIBLE:
                        self.agents[i].status = VACCINATED
                        self.agents[i].vaccination_wait_days_left= self.vaccine.immune_period
                    vax_used = vax_used + 1

            if vax_used >= self.vaccine.num_vaccine:
                break
        
        remaining_vaccines = self.vaccine.num_vaccine - vax_used
        #randomly vaccinate the rest of the population
        if remaining_vaccines > 0:
            for i in range(len(agents)):
                if self.agents[i].status == SUSCEPTIBLE:
                    self.agents[i].status = VACCINATED
                    self.agents[i].vaccination_wait_days_left= self.vaccine.immune_period
                    remaining_vaccines = remaining_vaccines - 1
                if remaining_vaccines == 0:
                    break

class Vaccine:
    def __init__(self, num_vaccine, effciency, reach_rate, immune_period):
        self.num_vaccine = num_vaccine
        self.effciency = effciency
        self.reach_rate = reach_rate
        self.immune_period = immune_period

class Ebola:
    def __init__(self):
        self.pr_base = 0.01962 
    
    
    def generate_incubation_period(self):
        return lognorm.rvs(s=0.284, scale=np.exp(2.446))
    
    
    def generate_infection_period(self):
        return lognorm.rvs(s=0.1332, scale=np.exp(2.2915))
    
    
    def generate_fatality(self):
        return bernoulli.rvs(0.85)
    

class Population:
    def __init__(self,
                 N,
                 family_size,
                 acquaintance_size,
                 scalar_factors_distribution):
        self.n_population = N
        self.family_size = family_size
        self.acquaintance_size = acquaintance_size
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
                )[0]
        
        # Household 
        random_list = list(range(self.n_population))
        np.random.shuffle(random_list)
        left = 0
        family_index = 0
        count = 0
        while left < self.n_population:
            
            right = left + 1 + np.random.poisson(lam=self.family_size)
            if right >= self.n_population:
                right = self.n_population
            family_member_indices = random_list[left:right]
            for family_member_index in family_member_indices:
                # Attribute: family_members
                agents[family_member_index].family_members = family_member_indices.copy()
                agents[family_member_index].family_members.remove(family_member_index)
                
                possible_acquaintances = random_list[:left] + random_list[right:]
                num_of_acquaintances = np.random.poisson(lam=self.acquaintance_size)
                acquaintances = random.sample(possible_acquaintances, num_of_acquaintances)
                agents[family_member_index].acquaintances = acquaintances
                
            left = right
        
        return agents



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

n_pop = 2000

pop = Population(N=n_pop, 
                 family_size=4, 
                 acquaintance_size=10,
                 scalar_factors_distribution=scalar_factors_distribution)
agents = pop.population_sample()


edge_sampler = EdgeSampler(agents,non_hh_contact_matrix=contact_matrix)
weight_sampler = WeightSampler(weight_dist)
vaccine = Vaccine(num_vaccine=30, effciency=0.998, reach_rate=0.7, immune_period=9)
ebola = Ebola()
simulation = DiseaseSimulation(agents,
                               200,
                               edge_sampler,
                               weight_sampler,
                               ebola,
                               vaccine)
simulation.initialize_seed_cases(10)

import time

start_time = time.time() #------------------------
res = simulation.run_simulation() 
end_time = time.time() #--------------------------

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")

res.to_csv("result.csv", sep=";")

plot = res[['susceptible', 'incubated', 'infected', 'deceased', 'removed']].div(n_pop).plot()
plot.set_xlabel("Day")
plot.set_ylabel("Ratio of population")
plot.set_title('Simulation')
plot.set_xticks(range(0, len(res), 20))
plt.show()

