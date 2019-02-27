class player():
    def __init__(self):
        import math
        pass
    
    def move(self, board, old_move, flag):
		cells = board.find_valid_move_cells(old_move)

    def minimax(board, old_mov, flag):

        cells = board.find_valid_move_cells(old_mov)
        
        optimum = 0
        if flag == 'minimiser':
            optimum = 1000000
        
        for i in cells:
            board.update(old_mov, i, )
            m = minimax(board, i, maximiser)
            if flag == 'minimiser':
                optimum = min(optimum, m)
            else:
                optimum = max(optimum, m)
                