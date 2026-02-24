from aima.agents import Agent
from aima.search import astar_search
from problems.drone_delivery_problem import DroneDeliveryProblem


class DroneAgent(Agent):
    """
    Agente de drone baseado em busca A* (AIMA compatible)
    """

    def __init__(self, environment):
        """
        environment : DroneEnvironment
        """

        # CRÍTICO: passar programa no construtor do Agent
        super().__init__(program=self.drone_program)

        self.environment = environment

        # plano atual
        self.plan = []

        # índice da ação atual
        self.current_action_index = 0

        # métricas
        self.total_cost = 0
        self.total_steps = 0

    # --------------------------------------------------

    def build_problem(self):
        """
        Constrói problema baseado no estado atual do ambiente
        """

        initial_state = (
            self.environment.drone_position,
            tuple(self.environment.remaining_deliveries)
        )

        return DroneDeliveryProblem(
            initial=initial_state,
            goal=(),
            grid_size=(self.environment.width, self.environment.height),
            obstacles=self.environment.obstacles
        )

    # --------------------------------------------------

    def generate_plan(self):
        """
        Executa A* para gerar plano
        """

        problem = self.build_problem()

        solution_node = astar_search(problem)

        if solution_node is None:
            print("Nenhuma solução encontrada.")
            return []

        plan = solution_node.solution()

        print("\nPlano gerado:", plan)

        return plan

    # --------------------------------------------------

    def drone_program(self, percept):
        """
        Programa principal do agente (AIMA required)
        percept = informação vinda do ambiente
        """

        # Se não há mais entregas, não faz nada
        if not self.environment.remaining_deliveries:

            print("\nTodas as entregas concluídas.")

            self.print_performance()

            return None

        # Se não tem plano, gera um
        if not self.plan:

            self.plan = self.generate_plan()
            self.current_action_index = 0

            if not self.plan:
                return None

        # Executa próxima ação
        if self.current_action_index < len(self.plan):

            action = self.plan[self.current_action_index]

            self.current_action_index += 1

            self.total_steps += 1
            self.total_cost += 1

            return action

        return None

    # --------------------------------------------------

    def reset_plan(self):

        self.plan = []
        self.current_action_index = 0

    # --------------------------------------------------

    def print_performance(self):

        print("\n===== PERFORMANCE DO AGENTE =====")

        print("Passos:", self.total_steps)
        print("Custo:", self.total_cost)