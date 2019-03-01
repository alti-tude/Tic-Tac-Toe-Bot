import time
from joblib import Memory

mem = Memory(cachedir='./tmp', verbose=1)

class player():
    def __init__(self):
        import math
        self.win_points = 10000
        self.lose_points = 10000
        self.draw_points = 0
        self.startTime = time.time()
        self.smallBoardUtil = {}
        self.maxTime = 23

        state = [['-' for j in range(3)] for i in range(3)]        
        self.SmallBoardUtility(state)
        # print self.smallBoardUtil['ooo------']
        # mem.cache()
    
    def move(self, board, old_mov, flag):
        if flag == 'o':
            flag = 'x' #assuming x is the maximiser
        self.startTime = time.time()

        depth = 1
        bestScore = -1000000
        opt_mov = -1
        while time.time() - self.startTime<self.maxTime:
            mov, score = self.minimax(board, old_mov, depth, 'maximiser',-1000000,1000000)
            depth += 1
            if bestScore<score:
                bestScore = score
                opt_mov = mov
        
        cells = board.find_valid_move_cells(old_mov)
        print cells
        print opt_mov
        print bestScore
        return opt_mov

    #flag is minimiser('o')/maximiser('x') depending on type of player
    def minimax(self, board, old_mov, depth, flag,alpha,beta):
        # print depth
        if depth == 0 or time.time()-self.startTime>self.maxTime:
            return old_mov, self.utility(board)
        win_status = board.find_terminal_state()
        # if  win_status == ('x','WON'):
        #     return old_mov, 10000
        # elif win_status == ('o','WON'):
        #     return old_mov, -10000
        # elif win_status == ('NONE', 'DRAW'):
        #     return old_mov, 0
        
        cells = board.find_valid_move_cells(old_mov)
        optimum = -100000
        opt_mov = -1
        if flag == 'minimiser':
            optimum = 1000000

        for cur_mov in cells:
            if flag == 'minimiser':
                _, won = board.update(old_mov, cur_mov, 'o')
                if won:
                    mov, m = self.minimax(board, cur_mov, depth-1, 'minimiser', alpha, beta)
                else:
                    mov, m = self.minimax(board, cur_mov, depth-1,'maximiser',alpha,beta)
                if optimum > m:
                    optimum = m
                    opt_mov = cur_mov
                beta = min( beta, optimum)
            else:
                _, won = board.update(old_mov, cur_mov, 'x')
                if won:
                    mov, m = self.minimax(board, cur_mov, depth-1, 'maximiser', alpha, beta)
                else:
                    mov, m = self.minimax(board, cur_mov, depth-1,'minimiser',alpha,beta)
                if optimum < m:
                    optimum = m
                    opt_mov = cur_mov
                alpha = max( alpha, optimum)

            board.big_boards_status[cur_mov[0]][cur_mov[1]][cur_mov[2]] = '-'
            board.small_boards_status[cur_mov[0]][cur_mov[1]//3][cur_mov[2]//3] = '-'

            if alpha<=beta or time.time()-self.startTime>self.maxTime:
                break

        return opt_mov, optimum

    def utility(self,board):
        # win_status = board.find_terminal_state()
        # if  win_status == ('x','WON'):
        #     return 10000
        # elif win_status == ('o','WON'):
        #     return -10000
        # elif win_status == ('NONE', 'DRAW'):
        #     return 0
        
        stateGridProb = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
        stateGridUtil = [[[k for k in range(3)] for i in range(3)] for j in range(2)]

        for k in range(2):
            for i in range(0,9,3):
                for j in  range(0,9,3):
                    a = [board.big_boards_status[k][i+p][j:j+3] for p in range(3)]
                    hashVal = self.hashSmallBoard(a)
                    num,den = self.smallBoardUtil[hashVal]
                    # print type(stateGridProb)
                    # print i//3
                    stateGridProb[k][i//3][j//3] = float(num)/float(den)
                    # print float(num)/float(den)
        
        for k in range(2):
            #centre
            mul = 1
            stateGridUtil[k][1][1] = 0
            for i in range(3): mul*=stateGridProb[k][1][i]
            stateGridUtil[k][1][1] += mul

            mul = 1
            for i in range(3): mul*=stateGridProb[k][i][1]
            stateGridUtil[k][1][1] += mul

            stateGridUtil[k][1][1] += stateGridProb[k][0][0]* stateGridProb[k][1][1]* stateGridProb[k][2][2]
            stateGridUtil[k][1][1] += stateGridProb[k][0][2]* stateGridProb[k][1][1]* stateGridProb[k][2][0]
            stateGridUtil[k][1][1] *= 3

            #corner
            for i in range(3):
                for j in range(3):
                    if j==1 or i==1: continue
                    mul = 1
                    stateGridUtil[k][i][j] = 0
                    for p in range(3): mul*=stateGridProb[k][i][p]
                    stateGridUtil[k][i][j] += mul

                    mul = 1
                    for i in range(3): mul*=stateGridProb[k][p][j]
                    stateGridUtil[k][i][j] += mul

                    stateGridUtil[k][i][j] += stateGridProb[k][i][j]*stateGridProb[k][1][1]* stateGridProb[k][2-i][2-j]
                    stateGridUtil[k][i][j] *= 4

            
            #others
            for i in range(3):
                for j  in range(3):
                    if i!=1 and j != 1: continue
                    mul = 1
                    stateGridUtil[k][i][j] = 0
                    for p in range(3): mul*=stateGridProb[k][i][p]
                    stateGridUtil[k][i][j] += mul

                    mul = 1
                    for i in range(3): mul*=stateGridProb[k][p][j]
                    stateGridUtil[k][i][j] += mul

                    stateGridUtil[k][i][j] *= 6
                    print stateGridUtil[k][i][j]


        #take sum of the utilities over the entire board
        total = 0
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    total += stateGridUtil[k][i][j]

        return total


    def hashSmallBoard(self,state):
        hashStr = ''.join([state[i][j] for i in range(3) for j in range(3)])
        return hashStr

    # @mem.cache
    def SmallBoardUtility(self, state):
        hashStr = self.hashSmallBoard(state)

        if hashStr in self.smallBoardUtil.keys():
            return self.smallBoardUtil[hashStr]
                     
        for i in state:
            if i == ['x','x','x']:
                self.smallBoardUtil[hashStr] = (1,1)
                return (1,1)

        for i in range(3):
            if [state[i][j] for j in range(3)] == ['x','x','x']:
                self.smallBoardUtil[hashStr] = (1,1)
                return (1,1)     
        
        if [state[0][0], state[1][1], state[2][2]] == ['x','x','x'] or [state[2][0], state[1][1], state[0][2]] == ['x','x','x']:
            self.smallBoardUtil[hashStr] = (1,1)
            return (1,1)

        for i in state:
            if i == ['o','o','o']:
                self.smallBoardUtil[hashStr] = (0,1)
                return (0,1)

        for i in range(3):
            if [state[i][j] for j in range(3)] == ['o','o','o']:
                self.smallBoardUtil[hashStr] = (0,1)
                return (0,1)     
        
        if [state[0][0], state[1][1], state[2][2]] == ['o','o','o'] or [state[2][0], state[1][1], state[0][2]] == ['o','o','o']:
            self.smallBoardUtil[hashStr] = (0,1)
            return (0,1)

        win = 0
        tot = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] == '-':
                    state[i][j] = 'x'
                    a,b = self.SmallBoardUtility(state)
                    win+=a
                    tot+=b
                    state[i][j] = 'o'
                    a,b = self.SmallBoardUtility(state)
                    win+=a
                    tot+=b
                    state[i][j] = '-'

        if tot == 0:
            tot = 1
        self.smallBoardUtil[hashStr] = (win,tot)
        # print self.smallBoardUtil['xo-oxoxxo']

        return (win,tot)
