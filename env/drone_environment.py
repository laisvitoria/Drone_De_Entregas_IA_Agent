# env/drone_environment.py

from aima.agents import Environment


class DroneEnvironment(Environment):

    def __init__(self, width, height, deliveries, obstacles, recharge_points):

        super().__init__()

        self.width = width
        self.height = height

        self.base = (0, 0)

        self.drone_position = self.base

        self.deliveries = deliveries
        self.remaining_deliveries = list(deliveries)

        self.obstacles = obstacles

        self.recharge_points = recharge_points

        self.history = [self.drone_position]

        self.agents = []

    # ----------------------------

    def add_agent(self, agent):
        self.agents.append(agent)

    # ----------------------------

    def percept(self, agent):

        return {
            "position": self.drone_position,
            "deliveries": tuple(self.remaining_deliveries),
            "recharge_points": tuple(self.recharge_points)
        }

    # ----------------------------

    def execute_action(self, agent, action):

        moves = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        if action not in moves:
            return

        dx, dy = moves[action]

        x, y = self.drone_position

        new_position = (x + dx, y + dy)

        if not self.is_valid_position(new_position):
            return

        self.drone_position = new_position

        self.history.append(new_position)

        print("Drone moveu para:", new_position)

        # entrega
        if new_position in self.remaining_deliveries:

            self.remaining_deliveries.remove(new_position)

            print("Entrega realizada em:", new_position)

        # recarga
        if new_position in self.recharge_points:

            print("Drone recarregando em:", new_position)

    # ----------------------------

    def is_valid_position(self, position):

        x, y = position

        return (
            0 <= x < self.width and
            0 <= y < self.height and
            position not in self.obstacles
        )

    # ----------------------------

    def is_done(self):

        return len(self.remaining_deliveries) == 0

    # ----------------------------

    def step(self):

        for agent in self.agents:

            percept = self.percept(agent)

            action = agent.program(percept)

            self.execute_action(agent, action)

    # ----------------------------

    def run(self, steps=100):

        step_count = 0

        while not self.is_done() and step_count < steps:

            self.visualize()

            self.step()

            step_count += 1

        self.visualize()

        print("\nSimulação finalizada.")

    # ----------------------------

    def visualize(self):

        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]

        # base
        x, y = self.base
        grid[y][x] = 'S'

        # obstáculos
        for (x, y) in self.obstacles:
            grid[y][x] = '#'

        # recarga
        for (x, y) in self.recharge_points:
            grid[y][x] = 'R'

        # entregas pendentes
        for (x, y) in self.remaining_deliveries:
            grid[y][x] = 'D'

        # caminho
        for (x, y) in self.history:
            if grid[y][x] == '.':
                grid[y][x] = '*'

        # drone atual
        x, y = self.drone_position
        grid[y][x] = 'A'

        print("\nMAPA:")

        for row in grid:
            print(' '.join(row))

        print("Legenda: S=Base A=Drone D=Entrega R=Recarga #=Obstáculo *=Caminho")