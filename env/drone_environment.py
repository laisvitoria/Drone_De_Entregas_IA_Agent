from aima.agents import Environment

class DroneEnvironment(Environment):

    def __init__(self, mapa, problem):

        super().__init__()

        self.mapa = mapa
        self.problem = problem

        self.state = problem.initial

        self.step_count = 0

        self.history = set()
        self.history.add(problem.initial[0])

    # --------------------------------------------------

    def percept(self, agent):

        return self.state

    # --------------------------------------------------

    def execute_action(self, agent, action):

        if action == "NOOP":
            return

        self.state = self.problem.result(self.state, action)

        self.history.add(self.state[0])

        self.step_count += 1

        self.display()

    # --------------------------------------------------

    def run(self, agent, max_steps=100):

        self.display()

        for _ in range(max_steps):

            if self.problem.goal_test(self.state):

                print("Todas as entregas realizadas!")
                return

            percept = self.percept(agent)

            action = agent.program(percept)

            if action is None:
                print("Agente terminou.")
                return

            self.execute_action(agent, action)

    # --------------------------------------------------

    def display(self):

        (x, y), entregas, bateria = self.state

        print("\nPasso:", self.step_count)
        print("Bateria:", bateria)
        print()

        for i in range(len(self.mapa)):

            linha = ""

            for j in range(len(self.mapa[0])):

                pos = (i, j)

                if pos == (x, y):
                    linha += "A "

                elif pos in entregas:
                    linha += "D "

                elif pos in self.history:
                    linha += "* "

                else:
                    linha += self.mapa[i][j] + " "

            print(linha)

        print("-------------------")