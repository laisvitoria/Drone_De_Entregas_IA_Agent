from agentes.drone_agent import DroneAgent
from env.drone_environment import DroneEnvironment
from problems.drone_delivery_problem import DroneDeliveryProblem
from tests.test_drone import *

MAPA = [

    ['S', '.', '.', '.', 'D'],
    ['.', '#', '#', '.', '.'],
    ['.', '.', 'R', '.', '.'],
    ['D', '#', '.', '.', '.'],
    ['.', '.', '.', '.', 'D']

]

problem = DroneDeliveryProblem(

    mapa=MAPA,
    max_bateria=10

)

env = DroneEnvironment(MAPA, problem)

agent = DroneAgent(problem)

env.run(agent)

test_a_star_integro()
