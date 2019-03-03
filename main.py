import time
from joblib import Memory
from math import *
mem = Memory(cachedir='./tmp', verbose=1)

class player():
    def __init__(self):
        self.win_points = 10000
        self.lose_points = 10000
        self.maxInt = 10000000000000000
        self.draw_points = 0
        self.firstMove = 1
        self.startTime = time.time()
        self.smallBoardUtil = [-1 for i in range(3**9)]
        # self.bigBoardUtil = [(0,0,0,0,0) for i in range 3^^9]
        self.moveCount = 0
        self.isNotBonus = 1
        self.depth = 1
        self.maxTime = 23
        self.wts = [
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ]
        
        # n = raw_input("next string? ")
        # while n!= "z":
        #     print self.SmallBoardUtility(self.to2D(n))
        #     n = raw_input("next string? ")
    
    def move(self, board, old_mov, flag):
        if flag == 'o':
            p1 = 'o'
            p2 = 'x' 
        else:
            p1 = 'x'
            p2 = 'o'
        self.startTime = time.time()
        if self.firstMove == 1:
            state = [['-' for j in range(3)] for i in range(3)]    
            self.SmallBoardUtility(state, p1, p2)
        
        cells = board.find_valid_move_cells(old_mov)
        if old_mov == (-1,-1,-1):
            return (1,3,4)
        
        
        # if self.firstMove==1:
        #     self.firstMove = 0
        #     return cells[0]
        bestScore = -2*self.maxInt
        opt_mov = old_mov

        prev = 0
        prev_mov = old_mov
        while time.time() - self.startTime<self.maxTime:
            prev = bestScore    
            prev_mov = opt_mov
            print "prev mov = ", prev_mov, self.depth, bestScore
            print "================="
            mov, score = self.minimax(board, old_mov, self.depth,p1, p2, 'maximiser',-2*self.maxInt,2*self.maxInt, self.isNotBonus)
            self.depth+=1
            bestScore = score
            opt_mov = mov

        self.depth = 1    

        # n = raw_input("next?")
        a = (board.big_boards_status[prev_mov[0]][prev_mov[1]][prev_mov[2]], board.small_boards_status[prev_mov[0]][prev_mov[1]/3][prev_mov[2]/3])
        _, won = board.update(old_mov, prev_mov, p1)
        if won and self.isNotBonus:
            self.isNotBonus = 0
        elif self.isNotBonus == 0:
            self.isNotBonus = 1
        board.big_boards_status[prev_mov[0]][prev_mov[1]][prev_mov[2]] = a[0]
        board.small_boards_status[prev_mov[0]][prev_mov[1]/3][prev_mov[2]/3] = a[1]
        
        return prev_mov

    #flag is minimiser('o')/maximiser('x') depending on type of player
    def minimax(self, board, old_mov, depth, p1, p2, flag,alpha,beta, count):
        if depth == 0 or time.time()-self.startTime>self.maxTime:
            return old_mov, self.utility(board, p1, p2)
        win_status = board.find_terminal_state()
        if  win_status == (p1,'WON'):
            return old_mov, self.maxInt
        elif win_status == (p2,'WON'):
            return old_mov, -self.maxInt
        elif win_status == ('NONE', 'DRAW'):
            return old_mov, 0
        
        cells = board.find_valid_move_cells(old_mov)
        optimum = -2*self.maxInt
        opt_mov = old_mov
        if flag == 'minimiser':
            optimum = 2*self.maxInt

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

            board.big_boards_status[cur_mov[0]][cur_mov[1]][cur_mov[2]] = '-'
            board.small_boards_status[cur_mov[0]][cur_mov[1]/3][cur_mov[2]/3] = '-'

            if alpha>=beta or time.time()-self.startTime>self.maxTime:
                break

        # board.print_board()
        # print self.utility(board, p1, p2)
        # print optimum, flag, opt_mov
        return opt_mov, optimum

    def utility(self, board, p1, p2):
        tot = 0
        for k in range(2):
            sc = [[[0 for i in range(3)] for j in range(3)] for p in  range(2)]
            for i in range(0,9,3):
                for j in range(0,9,3):
                    a = [board.big_boards_status[k][p][j:j+3] for p in range(i,i+3)]
                    a = self.SmallBoardUtility(a, p1, p2)
                    if a == (0,1,1):
                        sc[0][i/3][j/3] = 10*self.wts[i/3][j/3]*a[4]
                        sc[1][i/3][j/3] = 0 
                    elif a == (1,0,1):
                        sc[0][i/3][j/3] = 0 
                        sc[1][i/3][j/3] = 10*self.wts[i/3][j/3]*a[3]
                    else:
                        sc[0][i/3][j/3] = self.wts[i/3][j/3]*a[4]
                        sc[1][i/3][j/3] = self.wts[i/3][j/3]*a[3]

            score = 0
            for i in range(3):
                lineProb1 = 1
                lineProb2 = 1
                for j in range(3):
                    lineProb1*=sc[0][i][j]
                    lineProb2*=sc[1][i][j]

                score+=(lineProb1-lineProb2)
    
            for i in range(3):
                lineProb1 = 1
                lineProb2 = 1
                for j in range(3):
                    lineProb1*=sc[0][j][i]
                    lineProb2*=sc[1][j][i]

                score+=(lineProb1-lineProb2)
            
            
            lineProb1 = 1
            lineProb2 = 1
            for i in range(3):
                lineProb1*=sc[0][i][i]
                lineProb2*=sc[1][i][i]
            score+=(lineProb1-lineProb2)

            lineProb1 = 1
            lineProb2 = 1
            for i in range(3):
                lineProb1*=sc[0][i][2-i]
                lineProb2*=sc[1][i][2-i]
            score+=(lineProb1-lineProb2)

            tot+=score
            # print "sasdsada", k, score

        # print tot
        return tot

       

    def hashVal(self, state):
        a = [state[i][j] for i in range(3) for j in range(3)]
        ret = 0
        for i in a:
            ret*=3
            if i=='x':
                ret+=1
            elif i=='o':
                ret+=2
            else:
                ret+=0
        return ret

    def to2D(self, hs):
        a = [list(hs[i:i+3]) for i in range(0,9,3)]
        print a
        return a

    def SmallBoardUtility(self, state, p1, p2):
        hashStr = self.hashVal(state)
        # print hashStr
        # print len(self.smallBoardUtil)
        if self.smallBoardUtil[hashStr]!=-1:
            return self.smallBoardUtil[hashStr]
                     
        for i in state:
            if i == [p1,p1,p1]:
                self.smallBoardUtil[hashStr] = (0,1,1,0,10000)
                return (0,1,1, 0,10000)

        for i in range(3):
            if [state[j][i] for j in range(3)] == [p1,p1,p1]:
                self.smallBoardUtil[hashStr] = (0,1,1, 0,10000)
                return (0,1,1, 0,10000)     
        
        if [state[0][0], state[1][1], state[2][2]] == [p1,p1,p1] or [state[2][0], state[1][1], state[0][2]] == [p1,p1,p1]:
            self.smallBoardUtil[hashStr] = (0,1,1, 0,10000)
            return (0,1,1, 0,10000)

        for i in state:
            if i == [p2,p2,p2]:
                self.smallBoardUtil[hashStr] = (1,0,1, 10000,0)
                return (1,0,1, 10000,0)

        for i in range(3):
            if [state[j][i] for j in range(3)] == [p2,p2,p2]:
                self.smallBoardUtil[hashStr] = (1,0,1, 10000,0)
                return (1,0,1, 10000,0)     
        
        if [state[0][0], state[1][1], state[2][2]] == [p2,p2,p2] or [state[2][0], state[1][1], state[0][2]] == [p2,p2,p2]:
            self.smallBoardUtil[hashStr] = (1,0,1, 10000,0)
            return (1,0,1, 10000,0)

        win = 0
        lose = 0
        tot = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] == '-':
                    state[i][j] = p1
                    c,a,b,_,_ = self.SmallBoardUtility(state, p1, p2)
                    win+=a
                    lose+=c
                    tot+=b
                    state[i][j] = p2
                    c,a,b,_,_ = self.SmallBoardUtility(state, p1, p2)
                    win+=a
                    lose+=c
                    tot+=b
                    state[i][j] = '-'

        if tot == 0:
            tot = 1
        self.smallBoardUtil[hashStr] = (lose,win,tot, int(float(lose)/float(tot)*10000),int(float(win)/float(tot)*10000))

        # print state,hashStr, self.smallBoardUtil[hashStr]
        # print self.smallBoardUtil['xo-oxoxxo']

        return (lose,win,tot, int(float(lose)/float(tot)*10000),int(float(win)/float(tot)*10000))
