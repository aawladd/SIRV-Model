from re import S
from jupyter_client import protocol_version
import mesa 
from sirv.agents import State,MyAgent
from sirv.model import SIRVModel 


VACCINATED_COLOR = "#FE6D24"
SUSCEPTIBLE_COLOR = "#FE6D24"
INFECTED_COLOR = "#FE0101"
RECOVERED_COLOR = "#01FCFE"


def person_portrayal(agent):
    if agent is None:
        return 

    portrayal = {}

    if isinstance(agent,MyAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        color = SUSCEPTIBLE_COLOR 

        if agent.state == State.SUSCEPTIBLE:
            color = SUSCEPTIBLE_COLOR
        if agent.state == State.RECOVERED_S or agent.state == State.RECOVERED_V:
            color = RECOVERED_COLOR
        if agent.state == State.INFECTED_V or agent.state == State.INFECTED_V:
            color = INFECTED_COLOR
        if agent.state == State.VACCINATED:
            color = VACCINATED_COLOR

        portrayal["color"] = color

    return portrayal 

model_params = {
    "N": mesa.visualization.Slider(
        "Population", 100, 100, 10000, description="Total Population"
    ),
    "num_vaccination": mesa.visualization.Slider(
        "Number of Vaccination", 100, 100, 10000, description="Vaccination Population"
    ),
    "beta": mesa.visualization.Slider(
        "Beta", value=0.833, min_value=0, max_value=1, step=0.1, description="Infection Rate"
    ),
}

canvas_element = mesa.visualization.CanvasGrid(person_portrayal, 20, 20, 500, 500)

model_bar = mesa.visualization.BarChartModule(
    [
        {"Label": "SUSCEPTIBLE", "Color": SUSCEPTIBLE_COLOR},
        {"Label": "VACCINATED", "Color": VACCINATED_COLOR},
        {"Label": "INFECTED", "Color": INFECTED_COLOR},
        {"Label": "RECOVERED", "Color": RECOVERED_COLOR},
    ]
)


server = mesa.visualization.ModularServer(
    SIRVModel,
    [canvas_element],
    "Mesa Charts",
    model_params=model_params,
)