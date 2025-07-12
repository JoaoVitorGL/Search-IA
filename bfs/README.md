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

class Node:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
```

### 3.2. Teste de Solubilidade

Esta função implementa uma verificação para determinar se o puzzle é solucionável. Ela calcula o número de inversões: uma inversão ocorre sempre que uma peça de maior valor aparece na lista antes de uma peça de menor valor (o espaço em branco, 0, é ignorado). A regra é:

- Se o número total de inversões for par, o quebra-cabeça tem solução.
- Se for ímpar, é impossível resolvê-lo.

```python
def is_solvable(state):
    puzzle_pieces = [tile for tile in state if tile != 0]
    inversions = 0
    for i in range(len(puzzle_pieces)):
        for j in range(i + 1, len(puzzle_pieces)):
            if puzzle_pieces[i] > puzzle_pieces[j]:
                inversions += 1
    return inversions % 2 == 0
```

### 3.3. Geração de Sucessores

Esta função recebe um estado e gera todos os estados sucessores válidos. Ela localiza o espaço em branco (0) e calcula os movimentos possíveis (Cima, Baixo, Esquerda, Direita), retornando uma lista de novos estados.

```python
def get_successors(state):
    successors = []
    blank_index = state.index(0)
    row, col = divmod(blank_index, 3)

    moves = [('Up', -1, 0), ('Down', 1, 0), ('Left', 0, -1), ('Right', 0, 1)]

    for move_name, d_row, d_col in moves:
        new_row, new_col = row + d_row, col + d_col

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state_list = list(state)
            new_blank_index = new_row * 3 + new_col
            new_state_list[blank_index], new_state_list[new_blank_index] = \
                new_state_list[new_blank_index], new_state_list[blank_index]
            successors.append((move_name, tuple(new_state_list)))
    return successors
```

### 3.4. BFS e Reconstrução de Caminho

Esta é a função principal que implementa o algoritmo BFS. Ela inicializa a fila (deque) com o nó inicial e o conjunto de visited. O laço while queue: executa a busca, retirando um nó da fila, gerando seus sucessores e adicionando os novos (não visitados) à fila. A busca termina quando o estado objetivo é encontrado ou a fila fica vazia (no caso de um quebra-cabeça insolúvel, se a verificação is_solvable não fosse usada).

```python
def solve_puzzle(initial_board):
    initial_state = initial_board
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    if not is_solvable(initial_state):
        return None, -1, "Puzzle is not solvable."

    if initial_state == goal_state:
        return [Node(initial_state)], 0, "The puzzle is already in the goal state."

    queue = deque([Node(initial_state)])
    visited = {initial_state}

    while queue:
        current_node = queue.popleft()

        for move, new_state in get_successors(current_node.state):
            if new_state not in visited:
                new_node = Node(state=new_state, parent=current_node, move=move, depth=current_node.depth + 1)

                if new_state == goal_state:
                    solution_path = reconstruct_path(new_node)
                    return solution_path, len(solution_path) - 1, "Solution found!"

                visited.add(new_state)
                queue.append(new_node)

    return None, -1, "Could not find a solution."
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
