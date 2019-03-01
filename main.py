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
        self.maxTime = 22

        state = [['-' for j in range(3)] for i in range(3)]    
        # state = [['o','-','x'],['x','-','o'],['o','x','x']]    
        self.SmallBoardUtility(state, 'x', 'o', 1)
        
        # n = raw_input("next string? ")
        # while n!= "z":
        #     print self.smallBoardUtil[n]
        #     n = raw_input("next string? ")
        # mem.cache()
    
    def move(self, board, old_mov, flag):
        if flag == 'o':
            p1 = 'o'
            p2 = 'x' 
        else:
            p1 = 'x'
            p2 = 'o'
        self.startTime = time.time()

        depth = 1
        bestScore = -10000000
        opt_mov = -1
        while time.time() - self.startTime<self.maxTime:
            mov, score = self.minimax(board, old_mov, depth,p1, p2, 'maximiser',-1000000,1000000, 1)
            depth += 1
            if bestScore<score:
                bestScore = score
                print score
                opt_mov = mov
        
        cells = board.find_valid_move_cells(old_mov)
        print cells
        print opt_mov
        print bestScore
        return opt_mov

    #flag is minimiser('o')/maximiser('x') depending on type of player
    def minimax(self, board, old_mov, depth, p1, p2, flag,alpha,beta, count):
        # print depth
        if depth == 0 or time.time()-self.startTime>self.maxTime:
            return old_mov, self.utility(board, p1, p2)
        win_status = board.find_terminal_state()
        if  win_status == (p1,'WON'):
            return old_mov, 1000000
        elif win_status == (p2,'WON'):
            return old_mov, -1000000
        elif win_status == ('NONE', 'DRAW'):
            return old_mov, 0
        
        cells = board.find_valid_move_cells(old_mov)
        optimum = -10000000
        opt_mov = old_mov
        if flag == 'minimiser':
            optimum = 10000000

        for cur_mov in cells:
            if flag == 'minimiser':
                _, won = board.update(old_mov, cur_mov, p2)
                if won and count!=0:
                    mov, m = self.minimax(board, cur_mov, depth-1,p1, p2, 'minimiser', alpha, beta, 0)
                else:
                    mov, m = self.minimax(board, cur_mov, depth-1,p1, p2,'maximiser',alpha,beta, 1)
                if optimum > m:
                    optimum = m
                    opt_mov = cur_mov
                    beta = min( beta, optimum)
            else:
                _, won = board.update(old_mov, cur_mov, p1)
                if won and count!=0:
                    mov, m = self.minimax(board, cur_mov, depth-1,p1, p2, 'maximiser', alpha, beta, 0)
                else:
                    mov, m = self.minimax(board, cur_mov, depth-1,p1, p2,'minimiser',alpha,beta, 1)
                if optimum < m:
                    optimum = m
                    opt_mov = cur_mov
                    alpha = max( alpha, optimum )
            # board.print_board()
            # print self.utility(board, p1, p2)
            # n = raw_input("next?")
            board.big_boards_status[cur_mov[0]][cur_mov[1]][cur_mov[2]] = '-'
            board.small_boards_status[cur_mov[0]][cur_mov[1]/3][cur_mov[2]/3] = '-'

            if  time.time()-self.startTime>self.maxTime:
                break

        return opt_mov, optimum

    def utility(self,board, p1, p2):
        win_status = board.find_terminal_state()
        if  win_status == (p1,'WON'):
            return 10000000
        elif win_status == (p2,'WON'):
            return -10000000
        elif win_status == ('NONE', 'DRAW'):
            return 0
        
        stateGridProbWin = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
        stateGridProbLose = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
        stateGridUtilWin = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
        stateGridUtilLose = [[[k for k in range(3)] for i in range(3)] for j in range(2)]

        for k in range(2):
            for i in range(0,9,3):
                for j in  range(0,9,3):
                    a = [board.big_boards_status[k][i+p][j:j+3] for p in range(3)]
                    hashVal = self.hashSmallBoard(a)
                    lose,win,den = self.smallBoardUtil[hashVal]
                    # print type(stateGridProb)
                    # print i//3
                    stateGridProbWin[k][i//3][j//3] = float(win)/float(den)
                    stateGridProbLose[k][i//3][j//3] = float(lose)/float(den)
                    # print float(num)/float(den)
        
        for k in range(2):
            #centre
            mul = 1
            stateGridUtilWin[k][1][1] = 0
            for i in range(3): mul*=stateGridProbWin[k][1][i]
            stateGridUtilWin[k][1][1] += mul
            mul = 1
            for i in range(3): mul*=stateGridProbLose[k][1][i]
            stateGridUtilLose[k][1][1] += mul            

            mul = 1
            for i in range(3): mul*=stateGridProbWin[k][i][1]
            stateGridUtilWin[k][1][1] += mul
            mul = 1
            for i in range(3): mul*=stateGridProbLose[k][i][1]
            stateGridUtilLose[k][1][1] += mul

            stateGridUtilWin[k][1][1] += stateGridProbWin[k][0][0]* stateGridProbWin[k][1][1]* stateGridProbWin[k][2][2]
            stateGridUtilWin[k][1][1] += stateGridProbWin[k][0][2]* stateGridProbWin[k][1][1]* stateGridProbWin[k][2][0]
            stateGridUtilWin[k][1][1] *= 3

            stateGridUtilLose[k][1][1] += stateGridProbLose[k][0][0]* stateGridProbLose[k][1][1]* stateGridProbLose[k][2][2]
            stateGridUtilLose[k][1][1] += stateGridProbLose[k][0][2]* stateGridProbLose[k][1][1]* stateGridProbLose[k][2][0]
            stateGridUtilLose[k][1][1] *= 3

            #corner
            for i in range(3):
                for j in range(3):
                    if j==1 or i==1: continue
                    mul = 1
                    stateGridUtilWin[k][i][j] = 0
                    for p in range(3): mul*=stateGridProbWin[k][i][p]
                    stateGridUtilWin[k][i][j] += mul

                    mul = 1
                    for i in range(3): mul*=stateGridProbWin[k][p][j]
                    stateGridUtilWin[k][i][j] += mul

                    stateGridUtilWin[k][i][j] += stateGridProbWin[k][i][j]*stateGridProbWin[k][1][1]* stateGridProbWin[k][2-i][2-j]
                    stateGridUtilWin[k][i][j] *= 4

                    mul = 1
                    stateGridUtilLose[k][i][j] = 0
                    for p in range(3): mul*=stateGridProbLose[k][i][p]
                    stateGridUtilLose[k][i][j] += mul

                    mul = 1
                    for i in range(3): mul*=stateGridProbLose[k][p][j]
                    stateGridUtilLose[k][i][j] += mul

                    stateGridUtilLose[k][i][j] += stateGridProbLose[k][i][j]*stateGridProbLose[k][1][1]* stateGridProbLose[k][2-i][2-j]
                    stateGridUtilLose[k][i][j] *= 4

            
            #others
            for i in range(3):
                for j  in range(3):
                    if i!=1 and j != 1: continue
                    mul = 1
                    stateGridUtilWin[k][i][j] = 0
                    for p in range(3): mul*=stateGridProbWin[k][i][p]
                    stateGridUtilWin[k][i][j] += mul

                    mul = 1
                    for i in range(3): mul*=stateGridProbWin[k][p][j]
                    stateGridUtilWin[k][i][j] += mul

                    stateGridUtilWin[k][i][j] *= 6

                    mul = 1
                    stateGridUtilLose[k][i][j] = 0
                    for p in range(3): mul*=stateGridProbLose[k][i][p]
                    stateGridUtilLose[k][i][j] += mul

                    mul = 1
                    for i in range(3): mul*=stateGridProbLose[k][p][j]
                    stateGridUtilLose[k][i][j] += mul

                    stateGridUtilLose[k][i][j] *= 6


        # print stateGridProb[0]
        # print stateGridProb[1]
        #take sum of the utilities over the entire board
        total = 0
        m1 = 10000000000
        m2 = -10000000000
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    m1 = min(m1, stateGridUtilWin[k][i][j])
                    m2 = max(m2, stateGridUtilLose[k][i][j])
                    # total += stateGridUtilWin[k][i][j]
                    # total -= stateGridUtilLose[k][i][j]

        total = m1-m2
        return m2


    def hashSmallBoard(self,state):
        hashStr = ''.join([state[i][j] for i in range(3) for j in range(3)])
        return hashStr

    # @mem.cache
    def SmallBoardUtility(self, state, p1, p2, depth):
        hashStr = self.hashSmallBoard(state)

        if hashStr in self.smallBoardUtil.keys():
            return self.smallBoardUtil[hashStr]
                     
        for i in state:
            if i == [p1,p1,p1]:
                self.smallBoardUtil[hashStr] = (0,1,1)
                return (0,1,1)

        for i in range(3):
            if [state[j][i] for j in range(3)] == [p1,p1,p1]:
                self.smallBoardUtil[hashStr] = (0,1,1)
                return (0,1,1)     
        
        if [state[0][0], state[1][1], state[2][2]] == [p1,p1,p1] or [state[2][0], state[1][1], state[0][2]] == [p1,p1,p1]:
            self.smallBoardUtil[hashStr] = (0,1,1)
            return (0,1,1)

        for i in state:
            if i == [p2,p2,p2]:
                self.smallBoardUtil[hashStr] = (1,0,1)
                return (1,0,1)

        for i in range(3):
            if [state[j][i] for j in range(3)] == [p2,p2,p2]:
                self.smallBoardUtil[hashStr] = (1,0,1)
                return (1,0,1)     
        
        if [state[0][0], state[1][1], state[2][2]] == [p2,p2,p2] or [state[2][0], state[1][1], state[0][2]] == [p2,p2,p2]:
            self.smallBoardUtil[hashStr] = (1,0,1)
            return (1,0,1)

        win = 0
        lose = 0
        tot = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] == '-':
                    state[i][j] = p1
                    c,a,b = self.SmallBoardUtility(state, p1, p2, depth+1)
                    win+=a
                    lose+=c
                    tot+=b
                    state[i][j] = p2
                    c,a,b = self.SmallBoardUtility(state, p1, p2, depth+1)
                    win+=a
                    lose+=c
                    tot+=b
                    state[i][j] = '-'

        if tot == 0:
            tot = 1
        self.smallBoardUtil[hashStr] = (lose/float(depth),win/float(depth),tot)
        # print hashStr, (lose,win,tot)
        # print self.smallBoardUtil['xo-oxoxxo']

        return (lose,win,tot)
