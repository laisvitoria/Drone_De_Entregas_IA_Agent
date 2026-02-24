# Drone_De_Entregas_IA_Agent

Este é um repositório reservado à criação de um agente de Inteligência Artificial endereçado a resolver um problema proposto pela equipe do projeto. Especificado de acordo com o proposto em sala de aula durante a disciplina de Inteligência Artificial ofertada pela Universidade Federal de Sergipe (UFS), campus São Cristóvão.

# Especificação do Problema

O problema consiste em projetar um agente inteligente (Drone) capaz de realizar a entrega de um pacote saindo de uma base (origem) até o destino final (cliente), de forma autônoma e otimizada.

Para estruturar o problema, utilizamos a modelagem PEAS:

P (Performance/Desempenho): Minimizar o tempo/distância de voo, economizar bateria, chegar ao destino correto e não colidir com obstáculos.

E (Environment/Ambiente): Espaço aéreo modelado como uma grade (grid/grafo) contendo a base de lançamento, o ponto de entrega e zonas de exclusão (prédios, montanhas, clima adverso).

A (Actuators/Atuadores): Rotores para movimentação (norte, sul, leste, oeste, pousar, decolar) e mecanismo de liberação do pacote.

S (Sensors/Sensores): GPS (para coordenadas no grid), sensor de proximidade/câmera (para obstáculos) e medidor de bateria.


O agente pode se movimentar na horizontal ou na vertical.

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


Cada movimento custa 1. 

def path_cost(self, cost_so_far, state1, action, state2):
        """
        Cada movimento custa 1 unidade.
        """

        return cost_so_far + 1


A função de  transição result(s,a) funciona da seguinte forma : ele retorna um novo estado onde a nova posição x ser a soma da posição x atual com a da ação e o mesmo para a coordenada y. Após isso, ele subtrair 1 da bateria e caso a nova coordenada seja igual ao destino ele armazena o valor True na variável "novo_entregou".

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


A função goal_test verifica se o drone entregou e voltou à base

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



# Classificação do Ambiente

De acordo com as propriedades clássicas do AIMA, o ambiente de teste deste drone é classificado majoritariamente como:

Completamente Observável (ou Parcialmente Observável, caso o drone descubra obstáculos apenas durante o voo).

Determinístico: As ações do drone (mover-se para um bloco adjacente) têm resultados previsíveis (assumindo que não estamos modelando ventos fortes imprevisíveis).

Sequencial: A ação atual afeta todas as ações futuras (a rota).

Estático: Os obstáculos (prédios, zonas de restrição) não mudam de lugar durante o voo.

Discreto: O mapa e as ações são tratados de forma finita e em etapas, através de uma grade de posições.

Único Agente: Apenas o nosso drone atua no ambiente em busca de seu objetivo.


# Arquitetura Ambiente

O ambiente foi estruturado computacionalmente como um sistema de coordenadas espaciais (grafo ou matriz bidimensional). Cada nó ou célula representa uma posição no espaço aéreo. Células marcadas com "#" são obstáculos (intransponíveis). O estado inicial é a coordenada de base e o estado objetivo (D) é a coordenada do cliente. Além disso, a célula marcada com R é o ponto de recarga.

MAPA = [
    ['S', '.', '.', '.', '.'],
    ['.', '#', '#', '.', '.'],
    ['.', '.', 'R', '.', '.'],
    ['.', '#', '.', '.', 'D'],
    ['.', '.', '.', '.', '.']
]


# Agente

O drone atua como um Agente Baseado em Objetivos (e, de certa forma, Baseado em Utilidade, pois busca a melhor rota, e não apenas qualquer rota). Ele mantém uma representação interna do mapa (estado), tem um objetivo claro (local de entrega) e utiliza algoritmos de busca para deliberar sobre a sequência de passos ideal antes de começar a agir.

# Programa do Agente

O ciclo de vida do agente segue a estrutura básica:

Formulação do Objetivo: Receber as coordenadas do destino.

Formulação do Problema: Mapear os estados (posições atuais) e ações possíveis.

Busca: Chamar o algoritmo  A* para encontrar a rota com o menor custo.

Execução: Retornar a sequência de ações (caminho) e executá-las no ambiente até alcançar a meta.

# Repositório aima-python (aimacode)

Este projeto utiliza como base o repositório oficial aimacode/aima-python, que implementa em Python os algoritmos descritos no livro Artificial Intelligence: A Modern Approach.
Utilizamos especificamente as classes e funções do módulo de busca (search.py) para definir a nossa subclasse de Problem e executar o motor de resolução sem precisar reinventar a roda.


# Algotitmo de Busca e Heurística

Para garantir eficiência na entrega, o algoritmo escolhido para a busca do caminho foi o A* (A-Estrela), pois ele é completo e ótimo em ambientes como este.A função de avaliação é dada por $f(n) = g(n) + h(n)$, onde:$g(n)$: Custo real percorrido da base até o nó atual $n$.$h(n)$: Custo estimado (heurística) do nó atual $n$ até o destino.Como o drone se move em um grid, a heurística utilizada foi a Distância de Manhattan calculada pela fórmula:$h(n) = |x_1 - x_2| + |y_1 - y_2|$

# Testes e Visualização

Os testes foram realizados configurando diferentes mapas, alterando a posição dos obstáculos e a distância entre a origem e o destino.
A visualização do trajeto do drone é feita através de [descreva aqui sua visualização: impressões no console/terminal, interface gráfica com Pygame, ou gráficos em Matplotlib mostrando o grid].

# Execução do Projeto


Para rodar este projeto na sua máquina, siga os passos abaixo:

Clone este repositório:

Bash
git clone https://github.com/laisvitoria/Drone_De_Entregas_IA_Agent/
Navegue até o diretório do projeto:

Bash
cd /Drone_De_Entregas_IA_Agent

Bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Bash
pip install -r requirements.txt
Execute o arquivo principal:

Bash
python main.py

# Referências

RUSSELL, Stuart; NORVIG, Peter. Inteligência Artificial: Uma Abordagem Moderna. 3ª/4ª ed.

Repositório aima-python: https://github.com/aimacode/aima-python

Aulas e materiais da disciplina de Inteligência Artificial - UFS, campus São Cristóvão.