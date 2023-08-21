import random 
import numpy as np
import json
import  pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import lognorm, bernoulli
from itertools import combinations

'''
How to use MESA to support Agent-Based Modeling

'''

# Agent status
SUSCEPTIBLE = 0
INCUBATED = 1
INFECTED = 2
VACCINATED = 3
REMOVED = 4
SURVIVED = 4
IMMUNE = 4
DEAD = 5

# Contact matrix for each age group
# 0 = Children, 1 = Adolescent, 2 = Adult 

def get_all_contacts(person):
    res = []
    for group in person:
        res.extend(person[group])
    return res
        


def edge_sampling(N, class_type: list, contact_matrix, HH_dict, non_HH_dict):
    """
    N: Total population.
    class_type: An array that represents the class type of all agents in the system (age, age group, sex)...
    contact_matrix: Contact matrix of different class types.
    HH_dict: Dictionary representation of each household.
    non_HH_dict: Dictionary representation of non-household acquaintances of each persons in the system.
    """
    
    edge = {}    
    #Initialization
    for i in range(N):
        edge[i] = {"household": [], "non_household": []}
    
    #Edge initialization for each family
    for family_index in HH_dict:
        for (i,j) in list(combinations(HH_dict[family_index], 2)):
            edge[i]["household"].append(j)
            edge[j]["household"].append(i)
            
    #Edge initialization for each non-household contact
    for i in non_HH_dict:
        for j_class_type in non_HH_dict[i]:
            num_of_contacts = np.random.poisson(contact_matrix[class_type[i]][j_class_type])
            if num_of_contacts > len(non_HH_dict[i][j_class_type]):
                num_of_contacts = len(non_HH_dict[i][j_class_type])
            
            edge[i]["non_household"].extend(random.sample(non_HH_dict[i][j_class_type], num_of_contacts))
    return edge


def weight_sampling(N, edge, contact_dist):
    contact = {}
    for group in contact_dist:
        contact[group] = {}

    weight = {}
    for i in edge:
        weight[i] = {}
        for group in edge[i]:
            for j in edge[i][group]:
                weight[i][j] = random.choices(contact_dist[group]["risk_ratio"], 
                                              contact_dist[group]["percentage"])[0]
    return weight 
        

def ring_based_vaccination(edge, 
                           weight, 
                           agent_status,
                           agent_vaccine_wait_period, 
                           agent_infected, 
                           pr_base, 
                           num_vaccine, 
                           reach_rate):
    
    risk = {}
    contacts = {}
    for i in agent_infected:
        contacts = get_all_contacts(edge[i])

    contacts_of_contacts = {}
    for j in contacts:
        sub_contacts = {}
        for group in edge[j]:
            contacts_of_contacts[j]= get_all_contacts(edge[j])
    
    for c in contacts:
        # Update risk for contacts if they are SUSCEPTIBLE
        if agent_status[c] == SUSCEPTIBLE:
            prob = pr_base  * weight[i][c]
            risk[c] = prob

        # Update risk for contacts of contacts if they are SUSCEPTIBLE
        for cc in contacts_of_contacts[c]:
            if agent_status[cc] == SUSCEPTIBLE:
                if cc in edge[c]["household"]:
                    # Household risk
                    subprob = pr_base * weight[c][cc]
                else:
                    # Non household risk
                    subprob = pr_base * pr_base * weight[i][c] * weight[c][cc]
                
                risk[cc] = subprob
        
    risk_sorted = dict(sorted(risk.items(), key=lambda item: item[1]))
    vax_used = 0
    for i in risk_sorted:
        if vax_used < num_vaccine:
            if bernoulli.rvs(reach_rate, 1 - reach_rate) == 1:
                if agent_status[i] == INCUBATED:
                    if bernoulli.rvs(0.0002, 1 - 0.0002) != 1:
                        
                        agent_status[i] = VACCINATED
                        agent_vaccine_wait_period = 9
                elif agent_status[i] == SUSCEPTIBLE:
                    agent_status[i] = VACCINATED
                    agent_vaccine_wait_period = 9
                vax_used = vax_used + 1

            
        
        if vax_used >= num_vaccine:
            break
    
    remaining_vaccines = num_vaccine - vax_used
    #randomly vaccinate the rest of the population
    if remaining_vaccines > 0:
        for i in range(N):
            if agent_status[i] == SUSCEPTIBLE:
                agent_status[i] = VACCINATED
                agent_vaccine_wait_period = 9
                remaining_vaccines = remaining_vaccines - 1
            if remaining_vaccines == 0:
                break
    
        
    # while remaining_vaccines > 0:
    #     i= random.choice(list(range(N)))
    #     if agent_status[i] == SUSCEPTIBLE:
    #         agent_status[i] = VACCINATED
    #         agent_vaccine_wait_period = 9
    #         remaining_vaccines = remaining_vaccines - 1
    #         print(remaining_vaccines)
    


def simulation(N, 
               T, 
               HH_dict, 
               non_HH_dict,
               contact_matrix, 
               class_type,
               num_vaccine, 
               num_seed_case, 
               pr_base,
               cfr):
    # Initializes arrays indicating agents belonging to each status
    agent_infected = []
    agent_dead = []
    agent_susceptible = []
    agent_removed = []
    
    # Final result
    res = pd.DataFrame({"day": [],
                        "susceptible": [],
                        "incubated": [],
                        "infected": [],
                        "dead": [],
                        "vaccinated": [],
                        "removed": []})
    res.set_index("day", inplace=True)
    
    
    # Initialize status, infectious period, incubation period, vaccine period, risk score arrays
    agent_status = [0] * N
    agent_infectious_period = [0] * N
    agent_incubation_period = [0] * N
    agent_vaccine_wait_period = [0] * N
    agent_risk_score = [0] * N
    
    # Initizlize seed cases
    agent_infected = random.sample(list(range(0, N)), num_seed_case)
    # Update seed cases
    for index in agent_infected:
        agent_status[index] = INFECTED
        agent_infectious_period[index] = lognorm.rvs(s=0.1332, scale=np.exp(2.2915))
        
    for day in range(T):
        # Sampling contact and risk ratio for each day
        edge = edge_sampling(N,
                             class_type=class_type,
                             contact_matrix=contact_matrix, 
                             HH_dict=HH_dict, 
                             non_HH_dict=non_HH_dict)
        edge_weight = weight_sampling(N,edge,contact_dist)
        
        # For every agents in the network:
        for i in range(N):
            # If they are infected and still infectious,
            if agent_status[i] == INFECTED and agent_infectious_period[i] > 0:
                # get a list of their contacts
                contacts = get_all_contacts(edge[i])
                # contacts_of_contacts = {}
                # for j in contacts:
                #     # For each contact, get a list of their contacts, they are called contacts of contacts
                #     sub_contacts = []
                #     sub_contacts = get_all_contacts(edge[j])
                #     contacts_of_contacts[j] = sub_contacts
            
                # For every contacts of them,
                for c in contacts:
                    # if that contact is susceptible, calculate their risk.
                    if agent_status[c] == SUSCEPTIBLE:
                        prob = pr_base * edge_weight[i][c]
                        # If they has contracted the disease, update their status and incubation time.
                        if bernoulli.rvs(prob) == 1:
                            agent_status[c] = INCUBATED
                            agent_incubation_period[c] = lognorm.rvs(s=0.284, scale=np.exp(2.446)) 
                            
                    # For each contact of contact, if they is susceptible, calculate their secondary risk
                    # for cc in contacts_of_contacts[c]:
                    #     if agent_status[cc] == SUSCEPTIBLE:
                    #         # If they is a household member of the contact:
                    #         if cc in edge[c]["household"]:
                    #             subprob = pr_base * edge_weight[c][cc]
                    #         else:
                    #         # If they is not a household member of the contact:
                    #             subprob = pr_base*pr_base * edge_weight[i][c] * edge_weight[c][cc]
                    #         # If they has contracted the disease, update their statusb)
                    #         if bernoulli.rvs(subprob) == 1:
                    #             agent_status[cc] = INCUBATED
                    #             agent_incubation_period[cc] = log_normal(2.446, 0.284)

                # Substract infetious period by 1
                agent_infectious_period[i] = agent_infectious_period[i] - 1

            # If they are infected and their infectious period has finished,
            if agent_status[i] == INFECTED and agent_infectious_period[i] <= 0:
                if bernoulli.rvs(cfr) == 1:
                    # they can die from the disease,
                    agent_status[i] = DEAD
                    agent_infected.remove(i)
                else:
                #   or recover.
                    agent_status[i] = SURVIVED
                    agent_infected.remove(i)

            # If they are incubated:
            if agent_status[i] == INCUBATED:
                # If the incubation has ended,
                if agent_incubation_period[i] <= 0:
                    # they becomes infectious, initialize their infectious time.  
                    agent_status[i] = INFECTED
                    agent_infected.append(i)
                    agent_infectious_period[i] = lognorm.rvs(s=0.1332, scale=np.exp(2.2915))
                else:
                # If not, substract incubation time by 1.
                    agent_incubation_period[i] = agent_incubation_period[i] - 1
            
            # If they has been vaccinated:
            if agent_status[i] == VACCINATED:
                # If the waiting time has ended, they is now immune 
                if agent_vaccine_wait_period[i] <= 0:
                    agent_status[i] = IMMUNE
                else:
                    # Else, substract waiting time by 1.
                    agent_vaccine_wait_period[i] = agent_vaccine_wait_period[i] - 1
            
            if agent_status[i] in (SUSCEPTIBLE, REMOVED, DEAD):
                pass
            
            
        ring_based_vaccination(edge,edge_weight,agent_status,9,agent_infected,pr_base,num_vaccine,reach_rate=0.7)
        count_status = [0, 0, 0, 0, 0, 0]
        
        # Count the number of agents having the same status.
        for status in agent_status:
            count_status[status] = count_status[status] + 1
            
        
        today = pd.DataFrame([{"day": day,
                               "susceptible": count_status[SUSCEPTIBLE],
                               "incubated": count_status[INCUBATED],
                               "infected": count_status[INFECTED],
                                "vaccinated": count_status[VACCINATED],
                               "removed": count_status[REMOVED],
                               "dead": count_status[DEAD],

                               }]) 
        res = pd.concat([res, today],ignore_index=True)
    
    return res


                   
def population_sample(N,
                       family_size,
                       acquaintance_size,
                       class_distribution):
    
    class_type = [0] * N
    HH_dict = {}
    non_HH_dict = {}
    
    # Classtype
    class_type = random.choices([0,1,2], class_distribution, k=N)
    
    
    # Household 
    random_list = list(range(N))
    np.random.shuffle(random_list)
    left = 0
    family_index = 0
    while left < N:
        right = left + 1 + np.random.poisson(lam=family_size)
        if right >= N:
            right = N
        HH_dict[family_index] = random_list[left:right]
        
        
        
        # non house hold
        for i in HH_dict[family_index]:
            possible_acquaintances = random_list[:left] + random_list[right:]
            num_of_acquaintances = np.random.poisson(lam=acquaintance_size)
            acquaintances = random.sample(possible_acquaintances, num_of_acquaintances)
            non_HH_dict[i] = {0: [], 1: [], 2: []}
            for acquaintance in acquaintances:
                non_HH_dict[i][class_type[acquaintance]].append(acquaintance)
                
            
        left = right + 1
        family_index = family_index + 1
        
    return class_type, HH_dict, non_HH_dict

contact_matrix = np.array([[0.2, 2.0, 1.2], [2.0, 3.6, 1.5], [1.2, 1.5, 5.3]])
contact_dist = {
    "household": {
        "percentage": [0.163, 
                       0.403, 
                       0.17, 
                       0.026, 
                       0.1, 
                       0.138],
        "risk_ratio": [9.7, 
                       8.3,
                       5.6,
                       4.9,
                       1.3,
                       1
                       ]
    },
    "non_household": {
        "percentage": [1],
        "risk_ratio": [2.45],
    },  
}

N = 3000
class_type, HH_dict, non_HH_dict = population_sample(N,
                                                     4,
                                                     10,
                                                     [1/3.0, 1/3.0, 1/3.0])


simu = simulation(N=N,
                  T=150,
                  HH_dict=HH_dict,
                  non_HH_dict=non_HH_dict,
                  contact_matrix=contact_matrix,
                  class_type=class_type,
                  num_vaccine = 10,
                  num_seed_case = 5,
                  pr_base=0.01962,
                  cfr=0.7)

simu.to_csv("result.csv", sep=";")

plot = simu[['susceptible', 'incubated', 'infected', 'dead', 'removed']] \
    .div(N) \
    .plot()
plot.set_xlabel("Day")
plot.set_ylabel("Ratio of population")
plot.set_title('Simulation')
plot.set_xticks(range(0, len(simu), 20))
plt.show()