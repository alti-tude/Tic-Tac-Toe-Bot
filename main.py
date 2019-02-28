class player():
    def __init__(self):
        import math
        self.win_points = 10000
        self.lose_points = 10000
        self.draw_points = 0
        pass
    
    def move(self, board, old_mov, flag):
        if flag == 'o':
            flag = 'x' #assuming x is the maximiser
        opt_mov, score = self.minimax(board, old_mov, 3, 'maximiser',-1000000,1000000)
        cells = board.find_valid_move_cells(old_mov)
        print cells
        print opt_mov
        return opt_mov

    #flag is minimiser('o')/maximiser('x') depending on type of player
    def minimax(self, board, old_mov, depth, flag,alpha,beta):
        if depth == 0:
            return old_mov, self.utility(board)
        win_status = board.find_terminal_state()
        if  win_status == ('x','WON'):
            return old_mov, 10000
        elif win_status == ('o','WON'):
            return old_mov, -10000
        elif win_status == ('NONE', 'DRAW'):
            return old_mov, 0
        
        cells = board.find_valid_move_cells(old_mov)
        optimum = -100000
        opt_mov = -1
        if flag == 'minimiser':
            optimum = 1000000

        to_break = 0
        for cur_mov in cells:
            
            if flag == 'minimiser':
                board.update(old_mov, cur_mov, 'o')
                mov, m = self.minimax(board, cur_mov, depth-1,'maximiser',alpha,beta)
                if optimum > m:
                    optimum = m
                    opt_mov = cur_mov
                beta = min( beta, optimum)
            else:
                board.update(old_mov, cur_mov, 'x')
                mov, m = self.minimax(board, cur_mov, depth-1,'minimiser',alpha,beta)
                if optimum < m:
                    optimum = m
                    opt_mov = cur_mov
                alpha = max( alpha, optimum)

            board.big_boards_status[cur_mov[0]][cur_mov[1]][cur_mov[2]] = '-'
            board.small_boards_status[cur_mov[0]][cur_mov[1]//3][cur_mov[2]//3] = '-'

            if alpha<=beta:
                break

        return opt_mov, optimum

    def utility(self,board):
        win_status = board.find_terminal_state()
        if  win_status == ('x','WON'):
            return 10000
        elif win_status == ('o','WON'):
            return -10000
        elif win_status == ('NONE', 'DRAW'):
            return 0
        
        co = 0
        for k in range(2):
            for i in range(9):
                for j in  range(9):
                    if board.big_boards_status[k][i][j] == 'o':
                        co -= 1
                    elif board.big_boards_status[k][i][j] == 'x':
                        co += 1
        return co
