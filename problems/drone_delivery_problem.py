from aima.search import Problem

class DroneDeliveryProblem(Problem):

    def __init__(self, mapa, max_bateria=20):

        self.mapa = mapa
        self.max_bateria = max_bateria

        self.linhas = len(mapa)
        self.colunas = len(mapa[0])

        self.base = None
        self.recargas = set()
        self.entregas = set()

        # extrair informações do mapa
        for i in range(self.linhas):
            for j in range(self.colunas):

                if mapa[i][j] == 'S':
                    self.base = (i, j)

                elif mapa[i][j] == 'R':
                    self.recargas.add((i, j))

                elif mapa[i][j] == 'D':
                    self.entregas.add((i, j))

        estado_inicial = (
            self.base,
            frozenset(self.entregas),
            self.max_bateria
        )

        super().__init__(estado_inicial)

    # --------------------------------------------------

    def actions(self, state):

        (x, y), entregas, bateria = state

        if bateria <= 0:
            return ["NOOP"]

        movimentos = {

            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)

        }

        validas = []

        for nome, (dx, dy) in movimentos.items():

            nx, ny = x + dx, y + dy

            if self.posicao_valida(nx, ny):

                validas.append(nome)

        return validas

    # --------------------------------------------------

    def result(self, state, action):

        if action == "NOOP":
            return state

        (x, y), entregas, bateria = state

        movimentos = {

            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)

        }

        dx, dy = movimentos[action]

        nx, ny = x + dx, y + dy

        nova_bateria = bateria - 1

        novas_entregas = set(entregas)

        if (nx, ny) in novas_entregas:
            novas_entregas.remove((nx, ny))

        if (nx, ny) in self.recargas:
            nova_bateria = self.max_bateria

        return (

            (nx, ny),
            frozenset(novas_entregas),
            nova_bateria

        )

    # --------------------------------------------------

    def goal_test(self, state):

        _, entregas, _ = state

        return len(entregas) == 0

    # --------------------------------------------------

    def path_cost(self, c, state1, action, state2):

        return c + 1

    # --------------------------------------------------

    def h(self, node):

        pos, entregas, bateria = node.state

        if not entregas:
            return 0

        return min(

            abs(pos[0] - ex) + abs(pos[1] - ey)

            for ex, ey in entregas

        )

    # --------------------------------------------------

    def posicao_valida(self, x, y):

        if x < 0 or x >= self.linhas:
            return False

        if y < 0 or y >= self.colunas:
            return False

        if self.mapa[x][y] == '#':
            return False

        return True