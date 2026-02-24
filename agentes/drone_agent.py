from aima.agents import Agent
from aima.search import astar_search


class DroneAgent(Agent):

    def __init__(self, problem):

        super().__init__()

        self.problem = problem

        self.plan = []

        # OBRIGATÓRIO no AIMA
        self.program = self.agent_program

    # --------------------------------------------------

    def agent_program(self, percept):

        """
        percept = estado atual do ambiente
        """

        # atualizar estado inicial do problema
        self.problem.initial = percept

        # se não houver plano, gerar novo
        if not self.plan:

            solution = astar_search(self.problem)

            if solution is None:
                print("Nenhuma solução encontrada")
                return None

            self.plan = solution.solution()

            print("Plano:", self.plan)

        # executar próxima ação
        if self.plan:

            return self.plan.pop(0)

        return None