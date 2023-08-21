import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def SEIRD(T: int,
          init_state: list,
         exposure_rate: float,
         infection_rate: float,
         recovery_rate: float,
         fatality_rate:float):
     
     
     res = pd.DataFrame({"day": [0],
                         "susceptible": [init_state[0]],
                         "exposed": [init_state[1]],
                         "infected": [init_state[2]],
                         "recovered": [init_state[3]],
                         "deceased": [init_state[4]]}) 
     res.set_index("day", inplace=True)
     for day in range(1, T):
          S = res["susceptible"][day - 1]
          E = res["exposed"][day - 1]
          I = res["infected"][day - 1]
          R = res["recovered"][day - 1]
          D = res["deceased"][day - 1]
          
          BSI = exposure_rate * S * I
          kE = infection_rate * sE
          yI = recovery_rate * I
          uI = fatality_rate * I
          
          S = S - BSI
          E = E + BSI - kE
          I = I + kE - (yI + uI)
          R = R + yI
          D = D + uI
          
          today = pd.DataFrame([{"day": day,
                              "susceptible": S,
                                "exposed": E,
                                "infected": I,
                                "recovered": R,
                                "deceased": D,}])
          res = pd.concat([res, today], ignore_index=True)
     return res

          
          
          
init_state = [995, 0, 5, 0, 0]
exposure_rate = 0.005
infection_rate = 1/11.542
fatality_rate = 0.8/9.9
recovery_rate = 1 - fatality_rate

simu = SEIRD(200, init_state, exposure_rate, infection_rate, recovery_rate, fatality_rate)

plot = simu[['susceptible', 'exposed', 'infected', 'recovered', 'deceased']].div(1000).plot()
plot.set_xlabel("Day")
plot.set_ylabel("Ratio of population")
plot.set_title('Simulation')
plot.set_xticks(range(0, len(simu), 20))
plt.show()


