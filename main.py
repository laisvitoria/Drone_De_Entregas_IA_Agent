from search import astar_search
from drone_delivery_problem import DroneDeliveryProblem

problem = DroneDeliveryProblem()

solution = astar_search(problem)

if solution:

    print("Solução encontrada:\n")

    for node in solution.path():
        print(node.state)

    print("\nTotal de passos:", len(solution.path()) - 1)

else:
    print("Sem solução.")