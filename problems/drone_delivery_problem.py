# problems/drone_delivery_problem.py

from aima.search import Problem
import math


class DroneDeliveryProblem(Problem):

    def __init__(self, initial, goal=(), grid_size=(10, 10), obstacles=None):
        """
        initial = (posição, entregas_restantes)

        exemplo:
        ((0,0), ((3,3),(7,2)))
        """

        super().__init__(initial, goal)

        self.width = grid_size[0]
        self.height = grid_size[1]

        self.obstacles = obstacles if obstacles else []

        self.moves = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

    # --------------------------------------------------

    def actions(self, state):

        position, deliveries = state

        valid = []

        for action, move in self.moves.items():

            new_position = (
                position[0] + move[0],
                position[1] + move[1]
            )

            if self.is_valid(new_position):
                valid.append(action)

        return valid

    # --------------------------------------------------

    def result(self, state, action):

        position, deliveries = state

        move = self.moves[action]

        new_position = (
            position[0] + move[0],
            position[1] + move[1]
        )

        deliveries = list(deliveries)

        if new_position in deliveries:
            deliveries.remove(new_position)

        return (new_position, tuple(deliveries))

    # --------------------------------------------------

    def goal_test(self, state):

        position, deliveries = state

        return len(deliveries) == 0

    # --------------------------------------------------

    def path_cost(self, c, state1, action, state2):

        return c + 1

    # --------------------------------------------------

    def h(self, node):

        position, deliveries = node.state

        if not deliveries:
            return 0

        return min(
            self.distance(position, d)
            for d in deliveries
        )

    # --------------------------------------------------

    def distance(self, a, b):

        return math.sqrt(
            (a[0] - b[0])**2 +
            (a[1] - b[1])**2
        )

    # --------------------------------------------------

    def is_valid(self, position):

        x, y = position

        return (
            0 <= x < self.width and
            0 <= y < self.height and
            position not in self.obstacles
        )