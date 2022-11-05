import numpy as np
from mesa import Model
from sirv.agents import MyAgent, State
from mesa.time import RandomActivation 
from mesa.space import MultiGrid # To make grid
from mesa.datacollection import DataCollector # Traking the agent

class SIRVModel(Model):
    """A model for infection spread."""
    
    def __init__(self, N=10,num_vaccination = 5,width=10, height=10,
                beta = 0.833,gamma = 1/3, delta = 3,eta = 0.3, effectiveness = 0.5):
        
        self.num_agents = N
        self.num_vaccination = num_vaccination
        
        
        #parameters
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.eta = eta
        self.effectiveness = effectiveness
        

        
        
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)



        self.running = True
        self.dead_agents = []
        
        # Agent Creation 
        for i in range(self.num_agents):
            if i < self.num_vaccination:
                a = MyAgent("V",i, self)
            else:
                a = MyAgent("S", i, self)
            self.schedule.add(a)
            
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            

            # If want to make some agent initially infected but here we take initially 
            if a.state == State.VACCINATED:
                infected = np.random.choice([0,1], p=[0.01,0.99])
                
                if infected == 0:
                    a.state = State.INFECTED_V

                
            elif a.state == State.SUSCEPTIBLE:
                infected = np.random.choice([0,1], p=[0.03,0.97])
                if infected == 0:
                    a.state = State.INFECTED_S

                
        # Collecting States of agent
        self.datacollector = DataCollector(
            #model_reporters={"Gini": compute_gini}, 
            agent_reporters={"State": "state"})
            
        
 
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self):
        for i in range(self.run_time):
            self.step()