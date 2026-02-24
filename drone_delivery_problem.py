"""
Drone Delivery Problem
Compatível com a biblioteca AIMA (astar_search)

Estado é definido como:
(x, y, bateria, entregou)

onde:
x, y        -> posição do drone
bateria     -> nível atual da bateria
entregou    -> boolean indicando se já entregou o pacote
"""

from search import Problem


# CONFIGURAÇÃO DO MAPA

MAPA = [
    ['S', '.', '.', '.', '.'],
    ['.', '#', '#', '.', '.'],
    ['.', '.', 'R', '.', '.'],
    ['.', '#', '.', '.', 'D'],
    ['.', '.', '.', '.', '.']
]

LINHAS = len(MAPA)
COLUNAS = len(MAPA[0])

BATERIA_MAX = 10


# LOCALIZAR ELEMENTOS DO MAPA

def encontrar(tipo):
    """Retorna a posição (x,y) de um elemento no mapa."""
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if MAPA[i][j] == tipo:
                return (i, j)
    return None


BASE = encontrar('S')
DESTINO = encontrar('D')

RECARGAS = {
    (i, j)
    for i in range(LINHAS)
    for j in range(COLUNAS)
    if MAPA[i][j] == 'R'
}


# MOVIMENTOS POSSÍVEIS

MOVIMENTOS = [
    (0, 1),    # direita
    (0, -1),   # esquerda
    (1, 0),    # baixo
    (-1, 0)    # cima
]


# FUNÇÕES AUXILIARES

def posicao_valida(x, y):
    """Verifica se posição é válida no mapa."""
    return (
        0 <= x < LINHAS and
        0 <= y < COLUNAS and
        MAPA[x][y] != '#'
    )


def distancia_manhattan(a, b):
    """Calcula distância Manhattan entre dois pontos."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# CLASSE DO PROBLEMA

class DroneDeliveryProblem(Problem):

    def __init__(self):
        """
        Inicializa o problema com o estado inicial.
        """
        estado_inicial = (
            BASE[0],        # x
            BASE[1],        # y
            BATERIA_MAX,    # bateria cheia
            False           # ainda não entregou
        )

        super().__init__(estado_inicial)


    # ACTIONS

    def actions(self, state):
        """
        Retorna lista de ações possíveis a partir do estado atual.
        Cada ação é um movimento (dx, dy).
        """

        x, y, bateria, entregou = state

        acoes = []

        if bateria <= 0:
            return acoes

        for dx, dy in MOVIMENTOS:

            nx = x + dx
            ny = y + dy

            if posicao_valida(nx, ny):
                acoes.append((dx, dy))

        return acoes


    # RESULT

    def result(self, state, action):
        """
        Retorna novo estado após aplicar ação.
        """

        x, y, bateria, entregou = state

        dx, dy = action

        nx = x + dx
        ny = y + dy

        nova_bateria = bateria - 1

        novo_entregou = entregou

        # verificar entrega
        if (nx, ny) == DESTINO:
            novo_entregou = True

        # verificar recarga
        if (nx, ny) in RECARGAS:
            nova_bateria = BATERIA_MAX

        return (
            nx,
            ny,
            nova_bateria,
            novo_entregou
        )


    # GOAL TEST

    def goal_test(self, state):
        """
        Objetivo é:
        - pacote entregue
        - drone voltou à base
        """

        x, y, bateria, entregou = state

        return (
            entregou and
            (x, y) == BASE
        )


    # PATH COST

    def path_cost(self, cost_so_far, state1, action, state2):
        """
        Cada movimento custa 1 unidade.
        """

        return cost_so_far + 1


    # HEURISTIC

    def heuristic(self, node):
        """
        Heurística usada pelo A*
        """

        x, y, bateria, entregou = node.state

        pos = (x, y)

        if not entregou:

            return (
                distancia_manhattan(pos, DESTINO) +
                distancia_manhattan(DESTINO, BASE)
            )

        else:

            return distancia_manhattan(pos, BASE)


    def h(self, node):
        return self.heuristic(node)