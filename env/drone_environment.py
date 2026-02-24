# env/drone_environment.py

from aima.agents import Environment
import matplotlib.pyplot as plt
import numpy as np


class DroneEnvironment(Environment):
    """
    Ambiente de drone de entregas em grade (AIMA compatible)
    """

    def __init__(self, width=10, height=10, deliveries=None, obstacles=None):

        super().__init__()

        self.width = width
        self.height = height

        # posição inicial do drone
        self.drone_position = (0, 0)

        # entregas
        self.deliveries = deliveries if deliveries else []
        self.remaining_deliveries = list(self.deliveries)

        # obstáculos
        self.obstacles = obstacles if obstacles else []

        # histórico do caminho
        self.history = [self.drone_position]

        # lista de agentes no ambiente (AIMA padrão)
        self.agents = []

    # --------------------------------------------------

    def add_agent(self, agent):
        """
        Adiciona agente ao ambiente (AIMA style)
        """

        self.agents.append(agent)

    # --------------------------------------------------

    def percept(self, agent):
        """
        Retorna percepto para o agente
        """

        return (
            self.drone_position,
            tuple(self.remaining_deliveries)
        )

    # --------------------------------------------------

    def execute_action(self, agent, action):
        """
        Executa ação do agente
        """

        if action is None:
            return

        x, y = self.drone_position

        moves = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        move = moves.get(action, (0, 0))

        new_position = (
            x + move[0],
            y + move[1]
        )

        if self.is_valid_position(new_position):

            self.drone_position = new_position

            self.history.append(new_position)

            print("Drone moveu para:", new_position)

            # verificar entrega
            if new_position in self.remaining_deliveries:

                self.remaining_deliveries.remove(new_position)

                print("Entrega realizada em:", new_position)

    # --------------------------------------------------

    def is_valid_position(self, position):

        x, y = position

        return (
            0 <= x < self.width and
            0 <= y < self.height and
            position not in self.obstacles
        )

    # --------------------------------------------------

    def is_done(self):

        return len(self.remaining_deliveries) == 0

    # --------------------------------------------------

    def step(self):
        """
        Executa um passo (AIMA standard)
        """

        for agent in self.agents:

            percept = self.percept(agent)

            action = agent.program(percept)

            self.execute_action(agent, action)

    # --------------------------------------------------

    def run(self, steps=1000):
        """
        Executa simulação completa (AIMA compatible)
        """

        step_count = 0

        while not self.is_done() and step_count < steps:

            self.step()

            step_count += 1

        print("\nSimulação finalizada.")
        print("Passos executados:", step_count)
