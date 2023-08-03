import random 
from scipy.stats import lognorm, bernoulli
import numpy as np
from itertools import combinations
import json

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
contact_matrix = np.array([[0.2, 2.0, 1.2], [2.0, 3.6, 1.5], [1.2, 1.5, 5.3]])

# HH_dict and non_house hold dict
HH_dict = {0: [1,2,3],
           1: [4,5,6,7],
           2: [8],
           3: [9,10],
           4: [11,12],
           5: [13,14]
}

non_HH_dict = {0: {0: [4,7],
                   1: [5,6],
                   2: [8,9,13]
},
               1: {0: [4],
                   1: [5, 6],
                   2: [8,12]
},
}

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


N = 5
class_type = [random.randint(0,2) for _ in range(N)]

def log_normal(mu, sigma):
    return lognorm.rvs(s=sigma, scale=np.exp(mu))

def bernoulli(p):
    return bernoulli.rvs(p)


def edge_sampling(N, class_type, contact_matrix, HH_dict, non_HH_dict):
    edge = {}
    
    #Initializatioon
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
    '''
    if in household:
        contact type distribution:
    if not in household:
        default: 2.45
    '''
    weight = {}
    for i in edge:
        weight[i] = {}
        for group in edge[i]:
            for j in edge[i][group]:
                weight[i][j] = random.choices(contact_dist[group]["risk_ratio"], 
                                              contact_dist[group]["percentage"])[0]
        
    return weight 
        

# edge = {}   
# contacts = edge[i]
# contacts_of_contacts = {}
# for j in contacts:
#     sub_contacts = edge[j]
#     for k in sub_contacts:
#         contacts_of_contacts[j].append(k)

# for c in contacts:
#     if agent_status[c] == SUSCEPTIBLE:
#         prob = 
        



# edge = edge_sampling(N, class_type, contact_matrix, HH_dict, non_HH_dict)
# weight = weight_sampling(N, edge, contact_dist)

# print(json.dumps(edge, indent=4))
    

            
            
    



def simulation(T, N, HH_dict, non_HH_dict, num_vaccine, num_seed_case, cfr):
    # Initializes arrays indicating agents belonging to each status
    agent_infected = []
    agent_dead = []
    agent_susceptible = []
    agent_removed = []
    
    # Initizlize seed cases
    agent_infected = random.sample(list(range(0, N)), num_seed_case)
    # Initialize status, infectious period, incubation period, vaccine period, risk score arrays
    agent_status = [0] * N
    agent_infectious_period = [0] * N
    agent_incubation_period = [0] * N
    agent_vaccine_wait_period = [0] * N
    agent_risk_score = [0] * N
    
    # Update seed cases
    for index in agent_infected:
        agent_status[index] = INFECTED
        agent_infectious_period = log_normal(2.2915, 0.1332)
        
    for day in range(T):
        edge = edge_sampling(HH_dict, non_HH_dict)
        edge_weight = weight_sampling(edge)

        for i in range(N):
            
            if agent_status[i] == INFECTED and agent_incubation_period[i] > 0:
                # If this agent is infectious, get a list of their contacts
                contacts = edge[i]
                contacts_of_contacts = []
                for j in contacts:
                    # For each contact, get a list of their contacts, they are called contacts of contacts
                    sub_contacts = edge[j]
                    for k in sub_contacts:
                        contacts_of_contacts[j].append(k)
            
                for c in contacts:
                    # For each contact, if they are susceptible, calculate their risk
                    if agent_status[c] == SUSCEPTIBLE:
                        prob = pr_base * edge_weight[i][c]
                        # If they has contracted the disease, update their status
                        if bernoulli(prob) == 1:
                            agent_status[c] = INCUBATED
                            agent_incubation_period = log_normal(2.446, 0.284)
                            
                    # For each contact of contact, if they is susceptible, calculate their secondary risk
                    for cc in contacts_of_contacts:
                        if agent_status[c] == SUSCEPTIBLE:
                            # If they is a household member of the contact:
                            if cc in hh_dict[c]:
                                subprob = pr_base * edge_weight[c][cc]
                            else:
                            # If they is not a household member of the contact:
                                subprob = pr_base*pr_base * edge_weight[i][c] * edge_weight[c][cc]
                            # If they has contracted the disease, update their status
                            if bernoulli(subprob) == 1:
                                agent_status[cc] = 1
                                agent_incubation_period[cc] = log_normal(2.446, 0.284)

                agent_infectious_period[i] = agent_infectious_period[i] - 1


            if agent_status[i] == INCUBATED:
                if agent_incubation_period[i] == 0:
                    agent_status[i] = INFECTED
                    agent_infectious_period = log_normal(2.2915, 0.1332)
                else:
                    agent_incubation_period[i] = agent_incubation_period[i] - 1
            
            if agent_status[i] == VACCINATED:
                if agent_vaccine_wait_period[i] == 0:
                    agent_status[i] = IMMUNE
                else:
                    agent_vaccine_wait_period[i] = agent_vaccine_wait_period[i] - 1
            
            if agent_status[i] in (SUSCEPTIBLE, REMOVED, DEAD):
                pass

        
                            
            
              
    