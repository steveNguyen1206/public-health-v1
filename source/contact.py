from agent import Agent
import random
import numpy as np



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
