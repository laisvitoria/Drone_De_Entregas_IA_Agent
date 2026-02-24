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
Aqui está uma proposta de texto detalhado explicando a implementação dos testes automatizados. Você pode incluir esse conteúdo no seu README.md, na documentação do projeto ou no seu relatório final da disciplina.

Documentação dos Testes Automatizados
Para garantir a robustez do agente inteligente e a correta modelagem do ambiente, implementamos uma suíte completa de testes automatizados utilizando o framework Pytest.

A modelagem do problema foi construída estendendo a classe base Problem do repositório AIMA (Artificial Intelligence: A Modern Approach). Como os algoritmos de busca (como o A*) dependem inteiramente das regras definidas por essa classe para explorar as rotas, é fundamental garantir que a transição de estados, as restrições físicas e as heurísticas funcionem perfeitamente.

Os testes foram divididos lógicamente em grupos de responsabilidade:

1. Inicialização e Mapeamento do Ambiente
O primeiro grupo de testes valida se a classe DroneDeliveryProblem consegue "ler" a matriz do mapa corretamente. Testamos se:

As dimensões (linhas e colunas) são calculadas de forma exata.

As coordenadas da Base (S), dos Pontos de Recarga (R) e das Entregas (D) são extraídas e armazenadas nas estruturas de dados corretas (como tuplas e sets).

O estado inicial é formatado corretamente, contendo a posição de largada, o conjunto de entregas pendentes e a bateria máxima.

2. Validação de Espaço e Limites Geográficos
Um erro comum em algoritmos de busca em grades é a tentativa de acessar índices fora da matriz (o famoso IndexError). Os testes de posicao_valida asseguram que:

O drone não tente ultrapassar as bordas superiores, inferiores e laterais do mapa (coordenadas negativas ou maiores que o tamanho da matriz).

Células marcadas como obstáculos (#) sejam corretamente identificadas como intransponíveis.

3. Delimitação de Ações Possíveis (actions)
Este bloco testa a capacidade do agente de reconhecer o que ele pode ou não fazer a partir de um determinado estado. Verificamos se:

No meio de um espaço aberto, o drone reconhece que pode se mover para as quatro direções (UP, DOWN, LEFT, RIGHT).

Nas bordas ou próximo a obstáculos, as ações que levariam a colisões são removidas da lista de possibilidades.

Restrição de Bateria: Se a bateria do drone chegar a zero, a única ação retornada deve ser NOOP (ficar parado/inativo), impedindo que o algoritmo de busca continue explorando caminhos impossíveis.

4. Dinâmica e Transição de Estados (result)
Aqui validamos a máquina de estados do ambiente. Dado um estado atual e uma ação escolhida, o ambiente deve gerar o estado futuro correto. Os testes asseguram que:

Um movimento simples reduz a bateria em 1 unidade.

Mover-se para a coordenada de uma entrega (D) remove aquele pacote específico da lista de entregas pendentes.

Mover-se para um ponto de recarga (R) restaura a bateria do drone de volta ao seu limite máximo.

5. Função Objetivo e Heurística (goal_test e h)
Para que o algoritmo A* seja eficiente e completo, a função de objetivo e a heurística devem estar impecáveis.

Objetivo: Garantimos que o teste de objetivo só retorne True quando a lista de entregas pendentes estiver absolutamente vazia (e, se necessário pela regra de negócio, o drone estiver de volta à base).

Heurística: Testamos se o cálculo da Distância de Manhattan está retornando o valor correto entre a posição atual do drone e a entrega mais próxima, guiando a busca do A* de forma otimizada.

6. Parametrização e Topologias Diversas
Para garantir que o nosso código não está "viciado" em resolver apenas um único mapa, utilizamos o recurso de Parametrização do Pytest (@pytest.mark.parametrize).
Injetamos dinamicamente diversos cenários diferentes no mesmo teste:

Mapas em formato de corredor estreito.

Labirintos complexos.

Campos abertos com múltiplas entregas.

Situações sem saída (onde o drone nasce encurralado por obstáculos).

Isso garante que a nossa modelagem matemática escale para qualquer desafio proposto na simulação sem quebrar a execução do código.

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