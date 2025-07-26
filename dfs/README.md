# 8-Queens Solver

Resolução do problema do 8-Queens usando **Busca em Profundidade (DFS)**.

---

## 1. Formulação do Problema

- **Estado Inicial**  
  Tabuleiro 8×8 representado por uma lista de comprimento 8. Cada índice é uma coluna e o valor é a linha da rainha nessa coluna. Posições sem rainha são marcadas como -1.
  - Tabuleiro vazio. Ex: `[-1, -1, -1, -1, -1, -1, -1, -1]`
  - Parcialmente preenchido. Ex: `[3, -1, -1, -1, -1, -1, -1, -1] ` para uma rainha em (linha=3, coluna=0).
- **Objetivo**  
  Preencher todas as 8 colunas com rainhas de forma que nenhuma se ataque.
- **Operadores**  
  Em cada coluna livre, posicionar uma rainha em uma linha que não seja atacada por rainhas já colocadas.
- **Função Sucessora**  
  Para a coluna atual, gera todos os tabuleiros possíveis inserindo a rainha em cada linha segura.

---

## 2. Técnica Utilizada: Busca em Profundidade (DFS)

- Explora os ramos da árvore de busca o mais fundo possível antes de retroceder (backtracking).
- Utiliza uma pilha (stack) explícita para gerenciar os nós (estados) a serem explorados. A natureza LIFO (Last-In, First-Out) da pilha é o que caracteriza o DFS.
- Cada elemento na pilha é uma tupla (board, col), representando um estado do tabuleiro e a próxima coluna a ser preenchida.
- A busca para assim que a primeira solução completa é encontrada.

### Fluxo geral:

1. Empilhar o estado inicial (tabuleiro_inicial, coluna_0).
2. Enquanto existir estado na pilha:
   - Desempilha o estado corrente e incrementa contador de nós.
   - Se a coluna ≥ 8, encontrou solução completa.
   - Se há rainha pré-existente na coluna, somente valida segurança e avança de coluna.
   - Caso contrário, tenta cada linha de 0 a 7, verificando se é seguro e empilhando novos tabuleiros.
3. Retorna o tabuleiro solução ou None se não houver.

## 3. Principais Trechos de Código

### 3.1. Classe EightQueens e Inicialização do Tabuleiro

A classe encapsula toda a lógica. O **init** configura o tabuleiro, que é a estrutura de dados central. A lista self.board armazena o estado, onde board[coluna] = linha.

```python
class EightQueens:
    def __init__(self, initial_queens=[]): # Construtor da classe
        self.initial_queens = initial_queens # Armazena a lista de rainhas iniciais fornecida, se houver
        self.board = [-1] * 8 # O índice da lista representa a coluna, o valor representa a linha
        self.node_counter = 0 # Inicializa o contador para número de nós criados/visitados
        self.solution = None # Inicializa a variável que armazenará a solução encontrada

        # Preenche o tabuleiro com as rainhas iniciais.
        for row, col in self.initial_queens: # Itera sobre a lista de rainha iniciais
            if 0 <= col < 8: # Verifica se está dentro dos limites do tabuleiro
                self.board[col] = row # Posiciona a rainha no tabuleiro, atribuindo a linha 'row' à coluna 'col'
```

### 3.2. Verificação de Ataque

Dado um tabuleiro e uma posição (row, col) para uma nova rainha, esta função verifica se a posição é segura. Como o algoritmo preenche coluna por coluna, a função só precisa checar as colunas à esquerda (c < col).

- Ataque na Linha: board[c] == row
- Ataque na Diagonal: abs(board[c] - row) == abs(c - col)

```python
    # Método para verificar se é seguro colocar uma rainha em uma determinada posição
    def is_safe(self, board, row, col):
        for c in range(col): # Itera sobre todas as colunas 'c' á esquerda da coluna 'col'
            if board[c] == row: # Verifica se há uma rainha na mesma linha
                return False # Se houver retorna, a posição não é segura, então retorna False
            if abs(board[c] - row) == abs(c - col): # Verifica se há uma rainha na mesma diagonal
                return False # Se houver retorna, a posição não é segura, então retorna False
        return True # Se o loop terminar sem encontrar ataques, retorna True
```

### 3.3. Algoritmo de Busca

Esta função implementa uma Busca em Profundidade (DFS) para encontrar a solução. Ela utiliza uma pilha para gerenciar os diferentes estados do tabuleiro.
O algoritmo funciona em um laço: retira um tabuleiro da pilha e avança para a próxima coluna vazia. Nela, tenta posicionar uma rainha em cada linha segura. Cada posicionamento válido gera um novo estado que é adicionado à pilha para ser explorado.
O processo se repete até que um tabuleiro com todas as rainhas posicionadas corretamente seja encontrado (a solução) ou até que a pilha se esgote, indicando que não há solução.

```python
def solve(self):
        stack = [] # Inicializa a pilha
        stack.append((list(self.board), 0)) # Adiciona o estado inicial à pilha para dar início à busca.

        # Laço principal da busca: continua enquanto houver estados para explorar na pilha.
        while stack:
            board, col = stack.pop() # Desempilha o estado atual para ser explorado.

            self.node_counter += 1 # Incrementa o contador de nós cada vez que um estado é processado

            # Se a coluna é >=8, todas as rainhas foram posicionadas com sucesso.
            if col >= 8:
                self.solution = board # Armazena o tabuleiro final
                return self.solution # Retorna a solução e encerra a busca.

            # Verifica se já existe uma rainha pré-posicionada na coluna atual (valor não é -1).
            if board[col] != -1:
                # Verifica se a rainha pré-posicionada está em uma posição segura em relação às anteriores
                if self.is_safe(board, board[col], col):
                    stack.append((board, col + 1)) # Se for seguro, empilha o estado atual, mas avançando para a próxima coluna
                continue # Se não for seguro, este ramo da busca é abandonado (não faz nada).

            # Geração de sucessores: Itera por todas as linhas da coluna atual (7 a 0)
            for row in range(7, -1, -1):
                if self.is_safe(board, row, col): # Verifica se colocar uma rainha na posição (row, col) é uma jogada segura
                    new_board = list(board) # Se for seguro, cria uma cópia do tabuleiro atual
                    new_board[col] = row # Coloca a rainha na nova posição (row, col)

                    stack.append((new_board, col + 1)) # Empilha o novo estado (novo tabuleiro e a próxima coluna a ser preenchida).

        # Se o laço terminar e a pilha estiver vazia, não há solução.
        self.solution = None
        return self.solution # Retorna None
```

## 4. Resultados Obtidos

```bash
Starting with an empty board.

Solution found!
 Q  .  .  .  .  .  .  .
 .  .  .  .  .  .  Q  .
 .  .  .  .  Q  .  .  .
 .  .  .  .  .  .  .  Q
 .  Q  .  .  .  .  .  .
 .  .  .  Q  .  .  .  .
 .  .  .  .  .  Q  .  .
 .  .  Q  .  .  .  .  .
[0, 4, 7, 5, 2, 6, 1, 3]

Total nodes created/visited: 114
------------------------------

Initial board with queens at (row, column): [(3, 0)]

Solution found!
 .  Q  .  .  .  .  .  .
 .  .  .  .  Q  .  .  .
 .  .  .  .  .  .  Q  .
 Q  .  .  .  .  .  .  .
 .  .  Q  .  .  .  .  .
 .  .  .  .  .  .  .  Q
 .  .  .  .  .  Q  .  .
 .  .  .  Q  .  .  .  .
[3, 0, 4, 7, 1, 6, 2, 5]

Total nodes created/visited: 28
------------------------------

Initial board with queens at (row, column): [(0, 0), (5, 1)]

Solution found!
 Q  .  .  .  .  .  .  .
 .  .  .  .  .  .  Q  .
 .  .  .  Q  .  .  .  .
 .  .  .  .  .  Q  .  .
 .  .  .  .  .  .  .  Q
 .  Q  .  .  .  .  .  .
 .  .  .  .  Q  .  .  .
 .  .  Q  .  .  .  .  .
[0, 5, 7, 2, 6, 3, 1, 4]

Total nodes created/visited: 33
------------------------------

Initial board with queens at (row, column): [(6, 0), (0, 3), (3, 7)]

Solution found!
 .  .  .  Q  .  .  .  .
 .  .  .  .  .  .  Q  .
 .  .  Q  .  .  .  .  .
 .  .  .  .  .  .  .  Q
 .  Q  .  .  .  .  .  .
 .  .  .  .  Q  .  .  .
 Q  .  .  .  .  .  .  .
 .  .  .  .  .  Q  .  .
[6, 4, 2, 0, 5, 7, 1, 3]

Total nodes created/visited: 44
------------------------------
```
