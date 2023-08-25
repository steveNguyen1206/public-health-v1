# Modules import
import random
import pandas as pd
import numpy as np
from scipy.stats import bernoulli, lognorm
# Custom modules
from agent import Agent
from contact import EdgeSampler, WeightSampler


# Constant definitions
SUSCEPTIBLE = 0
INCUBATED = 1
INFECTED = 2
VACCINATED = 3
REMOVED = 4
RECOVERED = 4
IMMUNE = 4
DECEASED = 5


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
                            contact = self.agents[contact_index]
                            if contact.status == SUSCEPTIBLE:
                                prob = self.disease.pr_base * weight[agent_index][contact_index]
                                if bernoulli.rvs(prob) == 1:
                                    contact.start_incubation(self.disease.generate_incubation_period())
                        
                            for sub_contact_type in edge[contact_index]:
                                for sub_contact_index in edge[contact_index][sub_contact_type]:
                                    sub_prob = self.disease.pr_base * self.disease.pr_base * weight[agent_index][contact_index] * weight[contact_index][sub_contact_index]
                                    if self.agents[sub_contact_index].status in [SUSCEPTIBLE]:
                                        if self.agents[contact_index].status == INFECTED:
                                            sub_prob = weight[contact_index][sub_contact_index] * self.disease.pr_base
                                        else:
                                            sub_prob = self.disease.pr_base * self.disease.pr_base * weight[agent_index][contact_index] * weight[contact_index][sub_contact_index]
                                        if sub_prob > 1:
                                            sub_prob = 1
                                        if (bernoulli.rvs(sub_prob) == 1):
                                            self.agents[sub_contact_index].start_incubation(self.disease.generate_incubation_period())    
                    
                    
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
        self.result_df = res
        return res
    
    def ring_based_vaccination(self,edge,weight,daily_infected):
        contacts=[]
        contacts_of_contacts=[]
        risk={}
        for  agent in daily_infected:
            for contact_type in edge[agent.id]:
                for contact_index in edge[agent.id][contact_type]:
                    contact = self.agents[contact_index]
                    if contact.status == SUSCEPTIBLE:
                        prob = self.disease.pr_base * weight[agent.id][contact_index]
                        risk[contact_index]=prob
                        contacts.append(contact)

        for  c in contacts:
            for cc_type in edge[c.id]:
                for cc_index in edge[c.id][cc_type]:
                    cc = self.agents[cc_index]
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
            for i in range(len(self.agents)):
                if self.agents[i].status == SUSCEPTIBLE:
                    self.agents[i].status = VACCINATED
                    self.agents[i].vaccination_wait_days_left= self.vaccine.immune_period
                    remaining_vaccines = remaining_vaccines - 1
                if remaining_vaccines == 0:
                    break


