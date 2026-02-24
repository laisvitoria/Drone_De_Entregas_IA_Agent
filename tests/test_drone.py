import pytest
from problems.drone_delivery_problem import DroneDeliveryProblem # Altere para o nome do seu arquivo

# ============================================
# MAPAS DE TESTE
# ============================================

MAPA_PADRAO = [
    ['S', '.', '.', 'R'],
    ['#', '#', '.', '.'],
    ['D', '.', '#', 'D']
]
# Base: (0,0)
# Recarga: (0,3)
# Entregas: (2,0), (2,3)
# Obstáculos: (1,0), (1,1), (2,2)

MAPA_VAZIO = [
    ['S', '.'],
    ['.', 'D']
]

# ============================================
# CLASSE AUXILIAR
# ============================================

class MockNode:
    def __init__(self, state):
        self.state = state

# ============================================
# GRUPO 1: INICIALIZAÇÃO E PARSING DO MAPA
# ============================================

def test_01_init_dimensoes_corretas():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.linhas == 3
    assert problema.colunas == 4

def test_02_init_encontra_base_corretamente():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.base == (0, 0)

def test_03_init_mapeia_multiplas_entregas_e_recargas():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert (2, 0) in problema.entregas
    assert (2, 3) in problema.entregas
    assert (0, 3) in problema.recargas
    assert len(problema.entregas) == 2
    assert len(problema.recargas) == 1

def test_04_init_estado_inicial_formatado_corretamente():
    problema = DroneDeliveryProblem(MAPA_VAZIO, max_bateria=15)
    # O estado inicial AIMA deve ser: (posicao, frozenset_entregas, bateria)
    assert problema.initial == ((0, 0), frozenset([(1, 1)]), 15)

# ============================================
# GRUPO 2: VALIDAÇÃO DE POSIÇÕES
# ============================================

def test_05_posicao_valida_espaco_livre():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.posicao_valida(0, 1) is True

def test_06_posicao_invalida_obstaculo():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.posicao_valida(1, 0) is False # '#' no mapa

def test_07_posicao_invalida_x_negativo():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.posicao_valida(-1, 0) is False

def test_08_posicao_invalida_y_negativo():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.posicao_valida(0, -1) is False

def test_09_posicao_invalida_fora_dos_limites_maximos():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    assert problema.posicao_valida(3, 0) is False # x máx é 2
    assert problema.posicao_valida(0, 4) is False # y máx é 3

# ============================================
# GRUPO 3: AÇÕES POSSÍVEIS (actions)
# ============================================

def test_10_actions_sem_bateria_retorna_noop():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado_sem_bateria = ((0, 1), frozenset([(2, 0)]), 0)
    assert problema.actions(estado_sem_bateria) == ["NOOP"]

def test_11_actions_meio_do_mapa_todas_direcoes_livres():
    mapa_aberto = [['.', '.', '.'], ['.', 'S', '.'], ['.', '.', '.']]
    problema = DroneDeliveryProblem(mapa_aberto)
    estado = ((1, 1), frozenset([]), 10)
    acoes = problema.actions(estado)
    # Pode ir para todos os 4 lados
    assert set(acoes) == {"UP", "DOWN", "LEFT", "RIGHT"}

def test_12_actions_canto_do_mapa_direcoes_restritas():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado = ((0, 0), frozenset([]), 10)
    acoes = problema.actions(estado)
    # Na base (0,0), não pode ir UP nem LEFT. DOWN é obstáculo no MAPA_PADRAO. 
    # Só sobra RIGHT.
    assert acoes == ["RIGHT"]

def test_13_actions_ignora_obstaculos():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    # Posição (0,1). DOWN (1,1) é obstáculo.
    estado = ((0, 1), frozenset([]), 10)
    acoes = problema.actions(estado)
    assert "DOWN" not in acoes

# ============================================
# GRUPO 4: TRANSIÇÃO DE ESTADOS (result)
# ============================================

def test_14_result_acao_noop_nao_altera_estado():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado = ((0, 1), frozenset([(2, 0)]), 0)
    novo_estado = problema.result(estado, "NOOP")
    assert novo_estado == estado

def test_15_result_movimento_simples_reduz_bateria():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado = ((0, 0), frozenset([(2, 0)]), 10)
    novo_estado = problema.result(estado, "RIGHT")
    
    pos, _, bateria = novo_estado
    assert pos == (0, 1)
    assert bateria == 9

def test_16_result_movimento_para_entrega_remove_pacote():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado = ((2, 1), frozenset([(2, 0), (2, 3)]), 10) # Faltam 2 entregas
    novo_estado = problema.result(estado, "LEFT")      # Move para (2,0)
    
    _, entregas, _ = novo_estado
    assert (2, 0) not in entregas
    assert (2, 3) in entregas # A outra entrega continua lá
    assert len(entregas) == 1

def test_17_result_movimento_para_recarga_restaura_bateria():
    problema = DroneDeliveryProblem(MAPA_PADRAO, max_bateria=20)
    estado = ((0, 2), frozenset([]), 2) # Bateria quase no fim
    novo_estado = problema.result(estado, "RIGHT") # Move para 'R' em (0,3)
    
    _, _, bateria = novo_estado
    assert bateria == 20 # Bateria voltou ao máximo

# ============================================
# GRUPO 5: TESTE DE OBJETIVO E CUSTO
# ============================================

def test_18_goal_test_falso_ainda_ha_entregas():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado = ((0, 0), frozenset([(2, 0)]), 10)
    assert problema.goal_test(estado) is False

def test_19_goal_test_verdadeiro_entregas_vazias():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    estado = ((2, 0), frozenset([]), 5)
    assert problema.goal_test(estado) is True

def test_20_path_cost_sempre_incrementa_um():
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    # Custo atual = 5. Indo de estado1 para estado2 com qualquer ação.
    novo_custo = problema.path_cost(5, "estado1", "RIGHT", "estado2")
    assert novo_custo == 6

# ============================================
# GRUPO 6: HEURÍSTICA (A*)
# ============================================

def test_21_h_retorna_zero_se_nao_ha_entregas(): # Bônus!
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    no = MockNode(((0, 0), frozenset([]), 10))
    assert problema.h(no) == 0

def test_22_h_calcula_menor_distancia_manhattan(): # Bônus 2!
    problema = DroneDeliveryProblem(MAPA_PADRAO)
    # Drone em (0,1). Entregas em (2,0) e (2,3).
    # Distância para (2,0) = |0-2| + |1-0| = 2 + 1 = 3
    # Distância para (2,3) = |0-2| + |1-3| = 2 + 2 = 4
    # A heurística deve retornar a menor distância (3).
    estado = ((0, 1), frozenset([(2, 0), (2, 3)]), 10)
    no = MockNode(estado)
    assert problema.h(no) == 3

# ============================================
# GRUPO 7: TESTANDO CENÁRIOS (MAPAS DIFERENTES)
# ============================================


# Definindo mapas com topologias bem diferentes
MAPA_CORREDOR = [
    ['#', '#', '#', '#', '#'],
    ['S', '.', 'R', '.', 'D'],
    ['#', '#', '#', '#', '#']
]

MAPA_LABIRINTO = [
    ['S', '#', 'D', '.', '.'],
    ['.', '#', '.', '#', '.'],
    ['.', '.', '.', '#', 'R']
]

MAPA_CAMPO_ABERTO = [
    ['S', '.', '.', '.'],
    ['.', '.', 'D', '.'],
    ['.', 'R', '.', 'D'],
    ['.', '.', '.', '.']
]

MAPA_SEM_SAIDA = [
    ['S', '#', 'D'],
    ['#', '#', '#']
]

# Lista de cenários no formato: (Mapa, Base Esperada, Qtd Entregas, Qtd Recargas, Linhas, Colunas)
CENARIOS = [
    (MAPA_CORREDOR, (1, 0), 1, 1, 3, 5),
    (MAPA_LABIRINTO, (0, 0), 1, 1, 3, 5),
    (MAPA_CAMPO_ABERTO, (0, 0), 2, 1, 4, 4),
    (MAPA_SEM_SAIDA, (0, 0), 1, 0, 2, 3)
]

@pytest.mark.parametrize("mapa, base, qtd_entregas, qtd_recargas, linhas, colunas", CENARIOS)
def test_23_diferentes_topologias_inicializacao(mapa, base, qtd_entregas, qtd_recargas, linhas, colunas):
    """Garante que a leitura do mapa funciona em qualquer formato ou layout."""
    problema = DroneDeliveryProblem(mapa)
    
    assert problema.base == base
    assert len(problema.entregas) == qtd_entregas
    assert len(problema.recargas) == qtd_recargas
    assert problema.linhas == linhas
    assert problema.colunas == colunas

@pytest.mark.parametrize("mapa", [MAPA_CORREDOR, MAPA_LABIRINTO, MAPA_CAMPO_ABERTO])
def test_24_diferentes_topologias_limites_do_mapa(mapa):
    """Garante que o drone nunca tente sair do mapa, não importa o tamanho dele."""
    problema = DroneDeliveryProblem(mapa)
    linhas = problema.linhas
    colunas = problema.colunas
    
    # Testando as 4 bordas extremas (sempre devem ser inválidas)
    assert problema.posicao_valida(-1, 0) is False            # Acima
    assert problema.posicao_valida(0, -1) is False            # Esquerda
    assert problema.posicao_valida(linhas, 0) is False        # Abaixo
    assert problema.posicao_valida(0, colunas) is False       # Direita

def test_25_drone_preso_sem_saida():
    """Testa um cenário onde o drone está cercado de obstáculos e não pode se mover."""
    problema = DroneDeliveryProblem(MAPA_SEM_SAIDA)
    estado_preso = ((0, 0), frozenset([(0, 2)]), 10) # Drone na base
    
    acoes = problema.actions(estado_preso)
    
    # Da posição (0,0), a direita (0,1) e abaixo (1,0) são '#'.
    # Acima e esquerda é fora do mapa. Logo, nenhuma ação deve ser possível além de ficar parado (caso tenha implementado) ou lista vazia.
    assert len(acoes) == 0 or acoes == ["NOOP"]