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
