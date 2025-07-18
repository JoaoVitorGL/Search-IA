# 8-Puzzle Solver

Resolução do problema do 8-Puzzle usando **Busca em Largura (BFS)** com poda de estados já avaliados.

---

## 1. Formulação do Problema

- **Estado Inicial**  
  Qualquer permutação de `(0,1,2,3,4,5,6,7,8)`.
- **Objetivo**  
  `(0,1,2,3,4,5,6,7,8)`
- **Operadores**  
  Movimentar o espaço em branco para cima, baixo, esquerda ou direita, quando possível.
- **Função Sucessora**  
  Gera todos os sucessores válidos trocando o `0 (espaço em branco)` com o tile adjacente.

---

## 2. Técnica Utilizada: Busca em Largura (BFS) com Poda

- Utiliza uma `deque` para explorar nós em largura, garantindo a menor quantidade de movimentos.
- Mantém um conjunto `visited` para não reexaminar estados já descobertos.
- Assim que alcança o estado objetivo, reconstrói o caminho até a raiz (nó inicial) e para a busca.

### Fluxo geral:

1. Enfileirar estado inicial.
2. Repetir até encontrar solução ou esgotar a fila:
   - Desenfileirar nó atual.
   - Gerar sucessores (`get_successors`).
   - Para cada sucessor não visitado:
     - Se for meta, reconstruir caminho e retornar.
     - Caso contrário, marcar como visitado e enfileirar.

---

## 3. Principais Trechos de Código

### 3.1. Classe Node

Esta classe é fundamental para a busca. Cada Node armazena não apenas o estado (state) do tabuleiro, mas também uma referência ao seu nó pai (parent), o movimento (move) que o gerou e a sua profundidade (depth) na árvore de busca. Isso é necessário para reconstruir o caminho da solução no final.

```python
from collections import deque

# Classe que define a estrutura de um nó na árvore de busca
class Node:
    def __init__(self, state, parent=None, move=None, depth=0): # Método construtor
        self.state = state # Estado do tabuleiro
        self.parent = parent # Referência ao nó pai
        self.move = move # O nome do movimento que levou do 'parent' a este 'state' (ex: 'Up', 'Down')
        self.depth = depth # Profundidade ou número de movimentos desde o nó inicial
```

### 3.2. Teste de Solubilidade

Esta função implementa uma verificação para determinar se o puzzle é solucionável. Ela calcula o número de inversões: uma inversão ocorre sempre que uma peça de maior valor aparece na lista antes de uma peça de menor valor (o espaço em branco, 0, é ignorado). A regra é:

- Se o número total de inversões for par, o quebra-cabeça tem solução.
- Se for ímpar, é impossível resolvê-lo.

```python
# Função que determina se uma configuração inicial do 8-Puzzle pode ser resolvida
def is_solvable(state):
    # Cria uma lista com todas as peças do tabuleiro, exceto o espaço em branco (0)
    puzzle_pieces = [tile for tile in state if tile != 0]
    inversions = 0 # Contador de inversões
    # Loop aninhado para comparar cada peça com todas as peças que vêm depois dela
    for i in range(len(puzzle_pieces)):
        for j in range(i + 1, len(puzzle_pieces)):
         # Uma inversão ocorre se uma peça que vem antes é maior que uma peça que vem depois
            if puzzle_pieces[i] > puzzle_pieces[j]:
                inversions += 1 # Incrementa o contador de inversões
    return inversions % 2 == 0 # O puzzle é solucionável se o número de inversões for par
```

### 3.3. Geração de Sucessores

Esta função recebe um estado e gera todos os estados sucessores válidos. Ela localiza o espaço em branco (0) e calcula os movimentos possíveis (Cima, Baixo, Esquerda, Direita), retornando uma lista de novos estados.

```python
# Função que gera todos os movimentos válidos a partir de um estado do tabuleiro
def get_successors(state):
    successors = [] # Lista para armazenar os estados sucessores
    blank_index = state.index(0) # Encontra o índice do espaço em branco
    # Converte o índice linear (0-8) em linhas e colunas
    row, col = divmod(blank_index, 3) # Divide o índice do espaço em branco pelo tamanho do tabuleiro, row recebe o resultado da divisão e col recebe o resto da divisão

   # Define os possíveis movimentos como uma tupla: (Nome do Movimento, delta_linha, delta_coluna)
    moves = [('Up', -1, 0), ('Down', 1, 0), ('Left', 0, -1), ('Right', 0, 1)]

   # Itera sobre cada movimento possível
    for move_name, d_row, d_col in moves:
        new_row, new_col = row + d_row, col + d_col # Calcula a nova posição da linha e da coluna do espaço em branco

      # Verifica se a nova posição está dentro dos limites do tabuleiro 3x3
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state_list = list(state) # Converte a tupla do estado para uma lista para poder modificar seus elementos
            new_blank_index = new_row * 3 + new_col # Calcula o novo índice linear a partir das novas coordenadas (linha, coluna)

            # Realiza a troca: move a peça para a posição antiga do espaço em branco e o espaço em branco para a nova posição
            new_state_list[blank_index], new_state_list[new_blank_index] = \
                new_state_list[new_blank_index], new_state_list[blank_index]

            # Adiciona o novo estado (convertido de volta para tupla) e o nome do movimento à lista de sucessores.
            successors.append((move_name, tuple(new_state_list)))

    return successors # Retorna a lista de sucessores gerados
```

### 3.4. BFS e Reconstrução de Caminho

Esta é a função principal que implementa o algoritmo BFS. Ela inicializa a fila (deque) com o nó inicial e o conjunto de visited. O laço while queue: executa a busca, retirando um nó da fila, gerando seus sucessores e adicionando os novos (não visitados) à fila. A busca termina quando o estado objetivo é encontrado ou a fila fica vazia (no caso de um quebra-cabeça insolúvel, se a verificação is_solvable não fosse usada).

```python
# Função para reconstruir o caminho da solução a partir do nó final
def reconstruct_path(node):
    path = [] # Lista para armazenar os nós do caminho
    # Loop que continua enquanto o nó atual não for o nó raiz (cujo pai é None)
    while node is not None:
        path.append(node) # Adiciona o nó atual ao início da lista do caminho
        node = node.parent  # Move para o nó pai para continuar o rastreamento para trás
    path.reverse() # A lista foi construída do fim para o começo, então ela é invertida
    return path # Retorna a lista 'path' agora na ordem correta (do estado inicial ao final)
```

```python
# Função principal que resolve o puzzle usando BFS
def solve_puzzle(initial_board):
    initial_state = initial_board # Estado inicial do puzzle
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8) # Estado objetivo

   # Verifica se o puzzle é solucionável
    if not is_solvable(initial_state):
        return None, -1, "Puzzle is not solvable." # Se não for, finaliza a busca imediatamente

   # Verifica se o puzzle já está resolvido.
    if initial_state == goal_state:
      # Se sim, retorna um caminho com apenas o nó inicial
        return [Node(initial_state)], 0, "The puzzle is already in the goal state."

    queue = deque([Node(initial_state)]) # Inicializa a fila (deque) com o nó inicial
    visited = {initial_state} # Inicializa um conjunto (set) para guardar os estados já visitados

   # Loop principal da BFS: continua enquanto houver nós na fila para explorar
    while queue:
        current_node = queue.popleft() # Remove o nó da frente da fila

         # Gera todos os estados sucessores do nó atual
        for move, new_state in get_successors(current_node.state):
            if new_state not in visited: # Verifica se o novo estado já foi visitado. Esta é a poda
               # Cria um novo nó para o estado sucessor
                new_node = Node(state=new_state, parent=current_node, move=move, depth=current_node.depth + 1)

               # Verifica se o novo estado é o estado objetivo
                if new_state == goal_state:
                    solution_path = reconstruct_path(new_node) # Se for, reconstrói o caminho da solução
                    # Retorna o caminho, o número de passos e a mensagem de sucesso
                    return solution_path, len(solution_path) - 1, "Solution found!"

                visited.add(new_state) # Se não for o objetivo, marca o novo estado como visitado
                queue.append(new_node) # Adiciona o novo nó ao final da fila para ser explorado futuramente

    return None, -1, "Could not find a solution." # Return de segurança (Opcional pois já é verificado no inicio se o puzzle tem solução)
```

## 4. Resultados Obtidos

```bash
--- Solving: Puzzle 1 ---
Initial Board:
   [4 6 2]
   [8 1 3]
   [7 5  ]

Puzzle is not solvable.
----------------------------

--- Solving: Puzzle 2 ---
Initial Board:
   [6 4 2]
   [8 1 3]
   [7 5  ]

Solution found!
  Total steps: 20

--- Step Sequence ---

Step 1: Move Up
   [6 4 2]
   [8 1  ]
   [7 5 3]

Step 2: Move Up
   [6 4  ]
   [8 1 2]
   [7 5 3]

Step 3: Move Left
   [6   4]
   [8 1 2]
   [7 5 3]

Step 4: Move Down
   [6 1 4]
   [8   2]
   [7 5 3]

Step 5: Move Left
   [6 1 4]
   [  8 2]
   [7 5 3]

Step 6: Move Up
   [  1 4]
   [6 8 2]
   [7 5 3]

Step 7: Move Right
   [1   4]
   [6 8 2]
   [7 5 3]

Step 8: Move Right
   [1 4  ]
   [6 8 2]
   [7 5 3]

Step 9: Move Down
   [1 4 2]
   [6 8  ]
   [7 5 3]

Step 10: Move Down
   [1 4 2]
   [6 8 3]
   [7 5  ]

Step 11: Move Left
   [1 4 2]
   [6 8 3]
   [7   5]

Step 12: Move Up
   [1 4 2]
   [6   3]
   [7 8 5]

Step 13: Move Right
   [1 4 2]
   [6 3  ]
   [7 8 5]

Step 14: Move Down
   [1 4 2]
   [6 3 5]
   [7 8  ]

Step 15: Move Left
   [1 4 2]
   [6 3 5]
   [7   8]

Step 16: Move Left
   [1 4 2]
   [6 3 5]
   [  7 8]

Step 17: Move Up
   [1 4 2]
   [  3 5]
   [6 7 8]

Step 18: Move Right
   [1 4 2]
   [3   5]
   [6 7 8]

Step 19: Move Up
   [1   2]
   [3 4 5]
   [6 7 8]

Step 20: Move Left
   [  1 2]
   [3 4 5]
   [6 7 8]

--- End of Sequence ---
----------------------------

--- Solving: Puzzle 3 ---
Initial Board:
   [1 2 3]
   [  4 5]
   [6 7 8]

Solution found!
  Total steps: 13

--- Step Sequence ---

Step 1: Move Up
   [  2 3]
   [1 4 5]
   [6 7 8]

Step 2: Move Right
   [2   3]
   [1 4 5]
   [6 7 8]

Step 3: Move Right
   [2 3  ]
   [1 4 5]
   [6 7 8]

Step 4: Move Down
   [2 3 5]
   [1 4  ]
   [6 7 8]

Step 5: Move Left
   [2 3 5]
   [1   4]
   [6 7 8]

Step 6: Move Up
   [2   5]
   [1 3 4]
   [6 7 8]

Step 7: Move Left
   [  2 5]
   [1 3 4]
   [6 7 8]

Step 8: Move Down
   [1 2 5]
   [  3 4]
   [6 7 8]

Step 9: Move Right
   [1 2 5]
   [3   4]
   [6 7 8]

Step 10: Move Right
   [1 2 5]
   [3 4  ]
   [6 7 8]

Step 11: Move Up
   [1 2  ]
   [3 4 5]
   [6 7 8]

Step 12: Move Left
   [1   2]
   [3 4 5]
   [6 7 8]

Step 13: Move Left
   [  1 2]
   [3 4 5]
   [6 7 8]

--- End of Sequence ---
----------------------------

--- Solving: Puzzle 4 ---
Initial Board:
   [  1 2]
   [3 4 5]
   [6 7 8]

The puzzle is already in the goal state.
----------------------------
```
