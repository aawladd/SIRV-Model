from mesa import Agent
import enum
import numpy as np



class State(enum.IntEnum):
    SUSCEPTIBLE = 0
    VACCINATED = 1
    INFECTED_S = 2
    INFECTED_V = 3
    RECOVERED_S = 4
    RECOVERED_V = 5


class MyAgent(Agent):
    """ An agent in an epidemic model."""
    def __init__(self, SV,unique_id, model):
        super().__init__(unique_id, model)
        self.SV = SV
        if self.SV == "S":
            self.state = State.SUSCEPTIBLE
        else:
            self.state = State.VACCINATED 
#         self.infection_time = 0
    def move(self):
        """Move the agent"""

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    
    def status(self):
        """Check infection status"""
        
        if self.state == State.INFECTED_S: 
            recovery_rate_Is = self.model.gamma
            
            recovered = np.random.choice([0,1], p=[recovery_rate_Is,1-recovery_rate_Is])
            if recovered == 0:
                self.state = State.RECOVERED_S

                
        if self.state == State.INFECTED_V: 
            recovery_rate_Iv = self.model.gamma * self.model.delta
            
            recovered = np.random.choice([0,1], p=[recovery_rate_Iv,1-recovery_rate_Iv])
            if recovered == 0:
                self.state = State.RECOVERED_V

            

    def contact(self):
        """Find close contacts and infect"""
        
        cellmates = self.model.grid.get_cell_list_contents([self.pos])       
        if len(cellmates) > 1:

            for other in cellmates:
                
                    #If randomly not conntected with other agent
                if self.random.random() > self.model.beta:
                    continue
                    
                    #If Contatct Wtih Other agent
                if self.state is State.INFECTED_S and other.state is State.SUSCEPTIBLE:
                    rate = self.model.beta
                    decision = np.random.choice([0,1], p=[rate,1-rate])
                    
                    if decision == 0:
                        other.state = State.INFECTED_S
   
                        
                if self.state is State.INFECTED_S and other.state is State.VACCINATED:   
                    rate = self.model.beta * (1-self.model.eta)*self.model.effectiveness
                    decision = np.random.choice([0,1], p=[rate,1-rate])
                    
                    if decision == 0:
                        other.state = State.INFECTED_V

    
                if self.state is State.INFECTED_V and other.state is State.SUSCEPTIBLE:
                    rate = self.model.beta
                    decision = np.random.choice([0,1], p=[rate,1-rate])
                    
                    if decision == 0:
                        other.state = State.INFECTED_S

                    
                if self.state is State.INFECTED_S and other.state is State.VACCINATED:
                    rate = self.model.beta * (1-self.model.eta)*self.model.effectiveness
                    decision = np.random.choice([0,1], p=[rate,1-rate])
                    
                    if decision == 0:
                        other.state = State.INFECTED_V
                    
    def step(self):
        self.status()
        self.move()
        self.contact()