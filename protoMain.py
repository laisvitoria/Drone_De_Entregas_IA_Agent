import heapq
# ============================================
# CONFIGURAÇÃO DO MAPA
# ============================================
MAPA = [ ['S', '.', '.', '.', '.'],
         ['.', '#', '#', '.', '.'],
         ['.', '.', 'R', '.', '.'],
         ['.', '#', '.', '.', 'D'],
         ['.', '.', '.', '.', '.']]
LINHAS = len(MAPA)
COLUNAS = len(MAPA[0])
BATERIA_MAX = 10
# ============================================
# LOCALIZAR ELEMENTOS
# ============================================
def encontrar(tipo):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if MAPA[i][j] == tipo:
                return (i, j)
BASE = encontrar('S')
DESTINO = encontrar('D')
RECARGAS = set()
for i in range(LINHAS):
    for j in range(COLUNAS):
        if MAPA[i][j] == 'R':
            RECARGAS.add((i, j))
# ============================================
# ESTADO
# ============================================
class Estado:
    def __init__(self, x, y, bateria, entregou):
        self.x = x
        self.y = y 
        self.bateria = bateria 
        self.entregou = entregou
    def __eq__(self, other):
        return (
        	(self.x, self.y, self.bateria, self.entregou) == 
        	(other.x, other.y, other.bateria, other.entregou))
    def __hash__(self):
        return hash((self.x, self.y, self.bateria, self.entregou))
    def __lt__(self, other):
        return False
# ============================================
# FUNÇÕES AUXILIARES
# ============================================
def valido(x, y):
    return ( 0 <= x < LINHAS and 0 <= y < COLUNAS and MAPA[x][y] != '#' )
def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
# ============================================
# HEURÍSTICA
# ============================================
def heuristica(estado):
    pos = (estado.x, estado.y)
    if not estado.entregou:
        return distancia(pos, DESTINO) + distancia(DESTINO, BASE)
    else:
        return distancia(pos, BASE)
# ============================================
# TESTE DE OBJETIVO
# ============================================
def objetivo(estado):
    return ( estado.entregou and (estado.x, estado.y) == BASE )
# ============================================
# SUCESSORES
# ============================================
MOVIMENTOS = [ 
               (0, 1), # direita
               (0, -1), # esquerda
               (1, 0), # baixo 
               (-1, 0) # cima
             ]
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
        if (nx, ny) == DESTINO:
            entregou = True 
            if (nx, ny) in RECARGAS:
                nova_bateria = BATERIA_MAX 
                novo_estado = Estado( nx, ny, nova_bateria, entregou ) 
                lista.append(novo_estado) 
                return lista
# ============================================
# RECONSTRUIR CAMINHO
# ============================================
def reconstruir(came_from, atual):
    caminho = []
    while atual in came_from:
        caminho.append((atual.x, atual.y))
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
    heapq.heappush( open_list, (heuristica(inicio), 0, inicio) ) 
    came_from = {} 
    g_score = {} 
    g_score[inicio] = 0 
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
                heapq.heappush( open_list, (prioridade, novo_custo, vizinho) ) 
                came_from[vizinho] = atual 
                return None
# ============================================
# VISUALIZAÇÃO
# ============================================
def mostrar_caminho(caminho):
    mapa = [linha[:] for linha in MAPA] 
    for x, y in caminho:
        if mapa[x][y] == '.':
            mapa[x][y] = '*' 
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
        print("\nTotal de passos:", len(caminho) - 1) 
        mostrar_caminho(caminho) 
    else:
        print("Nenhuma solução encontrada.")
if __name__ == "__main__":
    main()
