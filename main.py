import time
from joblib import Memory
from math import *
mem = Memory(cachedir='./tmp', verbose=1)

class player():
    def __init__(self):
        self.win_points = 10000
        self.lose_points = 10000
        self.maxInt = 10000000000
        self.draw_points = 0
        self.startTime = time.time()
        self.smallBoardUtil = {}
        self.moveCount = 0
        self.isNotBonus = 1
        self.depth = 1
        self.maxTime = 23
        self.wts = [
            [4,3,4],
            [3,6,3],
            [4,3,4]
        ]
        state = [['-' for j in range(3)] for i in range(3)]    
        
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

        if old_mov == (-1,-1,-1):
            return (0,3,4)
        bestScore = -2*self.maxInt
        opt_mov = old_mov
        # if self.moveCount%5==0:
        #     self.moveCount = 0
        #     self.depth += 5
        # self.moveCount+=1
        prev = 0
        prev_mov = old_mov
        while time.time() - self.startTime<self.maxTime:
            prev = bestScore    
            prev_mov = opt_mov
            print "prev mov = ", prev_mov, self.depth
            print "================="
            mov, score = self.minimax(board, old_mov, self.depth,p1, p2, 'maximiser',-2*self.maxInt,2*self.maxInt, self.isNotBonus)
            self.depth+=1
            bestScore = score
            opt_mov = mov

        self.depth = 1    
        cells = board.find_valid_move_cells(old_mov)
        print cells
        print prev_mov, opt_mov
        print prev, bestScore
        print "movecount = ", self.moveCount
        # n = raw_input("next?")
        _, won = board.update(old_mov, prev_mov, p1)
        if won and self.isNotBonus:
            self.isNotBonus = 0
        elif self.isNotBonus == 0:
            self.isNotBonus = 1
        board.big_boards_status[prev_mov[0]][prev_mov[1]][prev_mov[2]] = '-'
        board.small_boards_status[prev_mov[0]][prev_mov[1]/3][prev_mov[2]/3] = '-'
        
        return prev_mov

    #flag is minimiser('o')/maximiser('x') depending on type of player
    def minimax(self, board, old_mov, depth, p1, p2, flag,alpha,beta, count):
        # print depth
        if depth == 0 or time.time()-self.startTime>self.maxTime:
            # if time.time()-self.startTime
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
            sc = [[0 for i in range(3)] for j in range(3)]
            for i in range(0,9,3):
                for j in range(0,9,3):
                    a = [board.big_boards_status[k][p][j:j+3] for p in range(i,i+3)]
                    sc[i/3][j/3] = self.wts[i/3][j/3]*self.SmallBoardUtility(a, p1, p2)
            score = 0

            for i in range(3):
                counto = 0
                countx = 0
                countd = 0
                mulo = 1
                mulx = 1
                for j in range(3):
                    if board.small_boards_status[k][i][j] == p1:
                        countx+=1
                        mulx*=sc[i][j]
                    if board.small_boards_status[k][i][j] == p2:
                        counto+=1
                        mulo*=sc[i][j]
                    if board.small_boards_status[k][i][j] == 'd':
                        countd+=1
                if counto == 2 and countx == 0 and countd == 0:
                    score -= mulo
                if counto == 0 and countx == 2 and countd == 0:
                    score += mulx
                if counto == 3:
                    score = -self.maxInt
                    return score
                if countx == 3:
                    score = self.maxInt
                    return score
            
            for i in range(3):
                counto = 0
                countx = 0
                countd = 0
                mulo = 1
                mulx = 1
                for j in range(3):
                    if board.small_boards_status[k][j][i] == p1:
                        countx+=1
                        mulx*=sc[j][i]
                    if board.small_boards_status[k][j][i] == p2:
                        counto+=1
                        mulo*=sc[j][i]
                    if board.small_boards_status[k][j][i] == 'd':
                        countd+=1
                if counto == 2 and countx == 0 and countd == 0:
                    score -= mulo
                if counto == 0 and countx == 2 and countd == 0:
                    score += mulx
                if counto == 3:
                    score = -self.maxInt
                    return score
                if countx == 3:
                    score = self.maxInt
                    return score
            
            counto = 0
            countx = 0
            countd = 0
            mulo = 1
            mulx = 1
            for i in range(3):
                if board.small_boards_status[k][i][i] == p1:
                    countx+=1
                    mulx*=sc[i][i]
                if board.small_boards_status[k][i][i] == p2:
                    counto+=1
                    mulo*=sc[i][i]
                if board.small_boards_status[k][i][i] == 'd':
                    countd+=1
            if counto == 2 and countx == 0 and countd == 0:
                score -= mulo
            if counto == 0 and countx == 2 and countd == 0:
                score += mulx
            if counto == 3:
                score = -self.maxInt
                return score
            if countx == 3:
                score = self.maxInt
                return score
            
            counto = 0
            countx = 0
            countd = 0
            mulo = 1
            mulx = 1
            for i in range(3):
                if board.small_boards_status[k][i][2-i] == p1:
                    countx+=1
                    mulx*=sc[i][2-i]
                if board.small_boards_status[k][i][2-i] == p2:
                    counto+=1
                    mulo*=sc[i][2-i]
                if board.small_boards_status[k][i][2-i] == 'd':
                    countd+=1
            if counto == 2 and countx == 0 and countd == 0:
                score -= mulo
            if counto == 0 and countx == 2 and countd == 0:
                score += mulx
            if counto == 3:
                score = -self.maxInt
                return score
            if countx == 3:
                score = self.maxInt
                return score

            for i in range(3):
                for j in range(3):
                    score += sc[i][j]
            tot+=score

        # print tot
        return tot

       

    def hashVal(self, state):
        return ''.join([state[i][j] for i in range(3) for j in range(3)])

    def to2D(self, hs):
        a = [list(hs[i:i+3]) for i in range(0,9,3)]
        print a
        return a

    def SmallBoardUtility(self, state, p1, p2):
        hashStr = self.hashVal(state)
        if hashStr in self.smallBoardUtil.keys():
            return self.smallBoardUtil[hashStr]

        counto = 0
        countx = 0
        score = 0

        #rows
        for i in range(3):
            counto = 0
            countx = 0
            for j in range(3):
                if state[i][j] == p1:
                    countx+=1
                if state[i][j] == p2:
                    counto+=1

            if countx == 2 and counto == 0:
                score += 10
            if countx == 0 and counto == 2:
                score -= 10
            if countx == 3 and counto == 0:
                score = 100
                self.smallBoardUtil[hashStr] = score
                return score
            if countx == 0 and counto == 3:
                score = -100
                self.smallBoardUtil[hashStr] = score
                return score


        #columns
        for i in range(3):
            counto = 0
            countx = 0
            for j in range(3):
                if state[j][i] == p1:
                    countx+=1
                if state[j][i] == p2:
                    counto+=1

            if countx == 2 and counto == 0:
                score += 10
            if countx == 0 and counto == 2:
                score -= 10
            if countx == 3 and counto == 0:
                score = 100
                self.smallBoardUtil[hashStr] = score
                return score
            if countx == 0 and counto == 3:
                score = -100
                self.smallBoardUtil[hashStr] = score
                return score


        #diagonals
        counto = 0
        countx = 0
        for i in range(3):
            if state[i][i] == p1:
                    countx+=1
            if state[i][i] == p2:
                    counto+=1

        if countx == 2 and counto == 0:
            score += 10
        if countx == 0 and counto == 2:
            score -= 10
        if countx == 3 and counto == 0:
            score = 100
            self.smallBoardUtil[hashStr] = score
            return score
        if countx == 0 and counto == 3:
            score = -100
            self.smallBoardUtil[hashStr] = score
            return score

        counto = 0
        countx = 0
        for i in range(3):
            if state[i][2-i] == p1:
                    countx+=1
            if state[i][2-i] == p2:
                    counto+=1

        if countx == 2 and counto == 0:
            score += 10
        if countx == 0 and counto == 2:
            score -= 10
        if countx == 3 and counto == 0:
            score = 100
            self.smallBoardUtil[hashStr] = score
            return score
        if countx == 0 and counto == 3:
            score = -100
            self.smallBoardUtil[hashStr] = score
            return score

        for i in range(3):
            for j in range(3):
                if state[i][j] == p1:
                    score+=1
                if state[i][j] == p2:
                    score-=1

        self.smallBoardUtil[hashStr] = score
        return score