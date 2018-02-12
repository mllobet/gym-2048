import random

class Engine:
    """ 2048 Game class """

    def __init__(self, N=4, start_tiles=2, seed=None):
        self.N = N
        self.score = 0
        self.ended = False
        self.won = False
        self.last_move = '-'
        self.start_tiles = start_tiles
        self.board = [[0]*self.N for i in range(self.N)]
        self.merged = [[False]*self.N for i in range(self.N)]

        if seed:
            random.seed(seed)
        
        self.add_start_tiles()


    def reset_game(self):
        self.score = 0
        self.ended = False
        self.won = False
        self.last_move = '-'
        self.board = [[0]*self.N for i in range(self.N)]
        self.merged = [[False]*self.N for i in range(self.N)]
        
        self.add_start_tiles()


    def get_board(self):
        return self.board


    def add_start_tiles(self):
        for i in range(self.start_tiles):
            self.add_random()


    def add_random(self):
        empty_cells = []
        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.board[i][j] == 0:
                    empty_cells += [[i,j]]
        
        if empty_cells:
            cell = random.choice(empty_cells)
            self.board[cell[0]][cell[1]] = 2 if random.random() < 0.9 else 4


    def create_traversal(self, vector):
        v_x = list(range(0,self.N))
        v_y = list(range(0,self.N))

        if vector['x'] == 1:
            v_x.reverse() 
        elif vector['y'] == 1:
            v_y.reverse()
            
        return (v_y, v_x)


    def find_furthest(self, row, col, vector):
        """ finds furthest cell interactable (empty or same value) """
        found = False
        val = self.board[row][col]
        i = row + vector['y']
        j = col + vector['x']
        while i >= 0 and i < self.N and j >= 0 and j < self.N:
            val_tmp = self.board[i][j] 
            if self.merged[i][j] or (val_tmp != 0 and val_tmp != val):
                return (i - vector['y'], j - vector['x'])
            if val_tmp:
                return (i, j)
                
            i += vector['y']
            j += vector['x']
            
        return (i - vector['y'], j - vector['x'])


    def create_vector(self, direction):
        if direction == 0:
            return {'x': 0, 'y': -1}
        elif direction == 1:
            return {'x': 1, 'y': 0}
        elif direction == 2:
            return {'x': 0, 'y': 1}
        else:
            return {'x': -1, 'y': 0}


    def moves_available(self):
        moves = [False]*4
        for direction in range(4):
            dir_vector = self.create_vector(direction)
            traversal_y, traversal_x = self.create_traversal(dir_vector)        

            for row in traversal_y:
                for col in traversal_x:
                    val = self.board[row][col]

                    if val:
                        n_row, n_col = self.find_furthest(row, col, dir_vector)

                        if not ((n_row,n_col) == (row,col)):
                            n_val = self.board[n_row][n_col]
                            if (val == n_val and not self.merged[n_row][n_col]) or (n_val == 0):
                                moves[direction] = True

        return moves


    def move(self, direction):
        # up: 0, right: 1, down: 2, left: 3
        dir_vector = self.create_vector(direction)
        traversal_y, traversal_x = self.create_traversal(dir_vector)        
        self.last_move = str(direction)
        reward = 0

        moved = False
        for row in traversal_y:
            for col in traversal_x:
                val = self.board[row][col]

                if val:
                    n_row, n_col = self.find_furthest(row, col, dir_vector)

                    # if furthest is found
                    if not ((n_row, n_col) == (row,col)):
                        # merge
                        if val == self.board[n_row][n_col] and not self.merged[n_row][n_col]:
                            self.board[n_row][n_col] += val
                            self.board[row][col] = 0
                            self.merged[n_row][n_col] = True

                            reward += val*2
                            self.score += reward
                            self.won = (reward == 2048)
                            moved = True
                        # move
                        elif self.board[n_row][n_col] == 0:
                            self.board[n_row][n_col] += val
                            self.board[row][col] = 0

                            moved = True

        # reset merged flags
        self.merged = [[False]*self.N for i in range(self.N)]
        if moved:
            self.add_random()

        self.ended = not True in self.moves_available() or self.won 
        if self.ended and not self.won:
            reward = -1

        return reward, self.ended


    def __str__(self):
        max_len = len(str(max(max(self.board))))
        board_str = ""
        for row in self.board:
            padded_row = [str(cell).rjust(max_len) for cell in row]
            board_str += "{0} {1} {2} {3}\n".format(*padded_row)
        
        board_str += "Score: {}\n".format(self.score)
        board_str += "Move: {}\n".format(self.last_move)
        return board_str            

