import random 
import numpy as np
import json
import  pandas as pd
import matplotlib.pyplot as plt
import time

from agent import Agent
from diseases import Ebola
from vaccine import Vaccine
from contact import EdgeSampler, WeightSampler
from population import Population
from disease_simulation import DiseaseSimulation

class Simulation:
    def __init__(self):
        self.data_csv = None
        self.params = {}
    

    def init_params_from_json_str(self, json_str):
        self.json_params = json.loads(json_str)
    
    
    def get_contact_matrix(self):
        if "contact_matrix" in self.params.keys():
            contact_matrix = self.params.get("contact_matrix")
        else: # Default values
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
        
        return contact_matrix
    
    
    def get_scalar_factors_distribution(self):
        if "scalars_factor_distribution" in self.params.keys():
            scalar_factors_distribution = self.params.get("scalar_factors_distribution")
        else:
            scalar_factors_distribution = {
                "age_group": {
                    "values": ["children", "adolescent", "adult"],
                    "weights": [0.25,0.25,0.5]
                }
            }
        return scalar_factors_distribution
            
    
    def get_weight_dist(self):
        if "weight_dist" in self.params.keys():
            weight_dist = self.params.get("weight_dist")
        else:
            weight_dist = weight_dist = {
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
        return weight_dist
    
    
    def init_
    
    
    def run():
        
        
    
    
    
    
    
input_str = '''{
"incubation_period": {
"type": "random_normal",
"properties": {
"mu": "1.22",
"sigma": "0.25"
}
},
"infection_period": {
"type": "random-gamma",
"properties": {
"alpha": "0.23",
"beta": "-0.71"
}
},
"n_seed_case": {
"type": "fixed",
"properties": {
"value": "5"
}
},
"case_fatality_rate":{
"type": "bernoulli",
"properties":{
"p": "0.8"
}
}
}'''
