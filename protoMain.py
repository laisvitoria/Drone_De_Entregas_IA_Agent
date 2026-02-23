import heapq  # Biblioteca usada para implementar a fila de prioridade (heap)

# ============================================
# CONFIGURAÇÃO DO MAPA
# ============================================

MAPA = [
    ['S', '.', '.', '.', '.'],   # S = Base inicial
    ['.', '#', '#', '.', '.'],   # # = Obstáculo
    ['.', '.', 'R', '.', '.'],   # R = Ponto de recarga
    ['.', '#', '.', '.', 'D'],   # D = Destino da entrega
    ['.', '.', '.', '.', '.']
]

LINHAS = len(MAPA)          # Número de linhas do mapa
COLUNAS = len(MAPA[0])      # Número de colunas do mapa
BATERIA_MAX = 10            # Valor máximo de bateria do drone

# ============================================
# LOCALIZAR ELEMENTOS NO MAPA
# ============================================

def encontrar(tipo):
    # Percorre todo o mapa procurando um símbolo específico
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if MAPA[i][j] == tipo:
                return (i, j)

BASE = encontrar('S')        # Localização da base
DESTINO = encontrar('D')     # Localização do destino

RECARGAS = set()             # Conjunto de pontos de recarga

for i in range(LINHAS):
    for j in range(COLUNAS):
        if MAPA[i][j] == 'R':
            RECARGAS.add((i, j))

# ============================================
# DEFINIÇÃO DO ESTADO
# ============================================

class Estado:
    def __init__(self, x, y, bateria, entregou):
        self.x = x                # Posição linha
        self.y = y                # Posição coluna
        self.bateria = bateria    # Quantidade atual de bateria
        self.entregou = entregou  # Se já entregou ou não

    def __eq__(self, other):
        return (self.x, self.y, self.bateria, self.entregou) == \
               (other.x, other.y, other.bateria, other.entregou)

    def __hash__(self):
        return hash((self.x, self.y, self.bateria, self.entregou))

    def __lt__(self, other):
        return False  # Necessário para evitar erro no heap

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def valido(x, y):
    # Verifica se está dentro do mapa e não é obstáculo
    return 0 <= x < LINHAS and 0 <= y < COLUNAS and MAPA[x][y] != '#'

def distancia(a, b):
    # Distância de Manhattan (heurística)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ============================================
# HEURÍSTICA (A*)
# ============================================

def heuristica(estado):
    pos = (estado.x, estado.y)

    if not estado.entregou:
        # CORREÇÃO: Continua igual — calcula ida + volta
        return distancia(pos, DESTINO) + distancia(DESTINO, BASE)
    else:
        return distancia(pos, BASE)

# ============================================
# TESTE DE OBJETIVO
# ============================================

def objetivo(estado):
    # Objetivo: já entregou e voltou para base
    return estado.entregou and (estado.x, estado.y) == BASE

# ============================================
# MOVIMENTOS POSSÍVEIS
# ============================================

MOVIMENTOS = [
    (0, 1),   # Direita
    (0, -1),  # Esquerda
    (1, 0),   # Baixo
    (-1, 0)   # Cima
]

# ============================================
# GERAR SUCESSORES
# ============================================

def sucessores(estado):
    lista = []

    for dx, dy in MOVIMENTOS:
        nx = estado.x + dx
        ny = estado.y + dy

        if not valido(nx, ny):
            continue

        nova_bateria = estado.bateria - 1

        if nova_bateria < 0:
            continue

        entregou = estado.entregou

        # CORREÇÃO: Atualiza entrega se chegar no destino
        if (nx, ny) == DESTINO:
            entregou = True

        # CORREÇÃO: Se for ponto de recarga, recarrega bateria
        if (nx, ny) in RECARGAS:
            nova_bateria = BATERIA_MAX

        # CORREÇÃO PRINCIPAL:
        # Sempre criar o novo estado (antes só criava se fosse destino)
        novo_estado = Estado(nx, ny, nova_bateria, entregou)
        lista.append(novo_estado)

    return lista   # 🔧 Antes tinha return errado dentro do loop

# ============================================
# RECONSTRUIR CAMINHO
# ============================================

def reconstruir(came_from, atual):
    caminho = [(atual.x, atual.y)]

    # CORREÇÃO: antes estava retornando dentro do while
    while atual in came_from:
        atual = came_from[atual]
        caminho.append((atual.x, atual.y))

    caminho.reverse()
    return caminho

# ============================================
# ALGORITMO A*
# ============================================

def a_star():
    inicio = Estado(BASE[0], BASE[1], BATERIA_MAX, False)

    open_list = []
    heapq.heappush(open_list, (heuristica(inicio), 0, inicio))

    came_from = {}
    g_score = {inicio: 0}

    visitados = set()

    while open_list:
        _, custo, atual = heapq.heappop(open_list)

        if objetivo(atual):
            return reconstruir(came_from, atual)

        if atual in visitados:
            continue

        visitados.add(atual)

        for vizinho in sucessores(atual):
            novo_custo = g_score[atual] + 1

            if vizinho not in g_score or novo_custo < g_score[vizinho]:
                g_score[vizinho] = novo_custo
                prioridade = novo_custo + heuristica(vizinho)

                heapq.heappush(open_list, (prioridade, novo_custo, vizinho))
                came_from[vizinho] = atual

    # CORREÇÃO: return None agora está no lugar certo
    return None

# ============================================
# VISUALIZAÇÃO
# ============================================

def mostrar_caminho(caminho):
    mapa = [linha[:] for linha in MAPA]

    for x, y in caminho:
        if mapa[x][y] == '.':
            mapa[x][y] = '*'

    # CORREÇÃO: impressão fora do loop
    print("\nMapa com caminho:\n")
    for linha in mapa:
        print(" ".join(linha))

# ============================================
# EXECUÇÃO
# ============================================

def main():
    caminho = a_star()

    if caminho:
        print("Caminho encontrado:")
        print(caminho)
        print("Total de passos:", len(caminho) - 1)
        mostrar_caminho(caminho)
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
