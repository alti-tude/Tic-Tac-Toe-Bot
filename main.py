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

    def SmallBoardUtility(self, state, p1, p2, depth):
        hashStr = self.hashVal(state)

        if hashStr in self.smallBoardUtil.keys():
            return self.smallBoardUtil[hashStr]
                     
        for i in state:
            if i == [p1,p1,p1]:
                self.smallBoardUtil[hashStr] = (1,1)
                return (1,1)

        for i in range(3):
            if [state[j][i] for j in range(3)] == [p1,p1,p1]:
                self.smallBoardUtil[hashStr] = (1,1)
                return (1,1)     
        
        if [state[0][0], state[1][1], state[2][2]] == [p1,p1,p1] or [state[2][0], state[1][1], state[0][2]] == [p1,p1,p1]:
            self.smallBoardUtil[hashStr] = (1,1)
            return (1,1)

        for i in state:
            if i == [p2,p2,p2]:
                self.smallBoardUtil[hashStr] = (0,1)
                return (0,1)

        for i in range(3):
            if [state[j][i] for j in range(3)] == [p2,p2,p2]:
                self.smallBoardUtil[hashStr] = (0,1)
                return (0,1)     
        
        if [state[0][0], state[1][1], state[2][2]] == [p2,p2,p2] or [state[2][0], state[1][1], state[0][2]] == [p2,p2,p2]:
            self.smallBoardUtil[hashStr] = (0,1)
            return (0,1)

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
        self.smallBoardUtil[hashStr] = (lose,win,tot)
        # print hashStr, (lose,win,tot)
        # print self.smallBoardUtil['xo-oxoxxo']

        return (lose,win,tot)

#     #flag is minimiser('o')/maximiser('x') depending on type of player
#     def minimax(self, board, old_mov, depth, p1, p2, flag,alpha,beta, count):
#         # print depth
#         if depth == 0 or time.time()-self.startTime>self.maxTime:
#             return old_mov, self.utility(board, p1, p2)
#         win_status = board.find_terminal_state()
#         if  win_status == (p1,'WON'):
#             return old_mov, 1000000
#         elif win_status == (p2,'WON'):
#             return old_mov, -1000000
#         elif win_status == ('NONE', 'DRAW'):
#             return old_mov, 0
        
#         cells = board.find_valid_move_cells(old_mov)
#         optimum = -10000000
#         opt_mov = old_mov
#         if flag == 'minimiser':
#             optimum = 10000000

#         for cur_mov in cells:
#             if flag == 'minimiser':
#                 _, won = board.update(old_mov, cur_mov, p2)
#                 if won and count!=0:
#                     mov, m = self.minimax(board, cur_mov, depth-1,p1, p2, 'minimiser', alpha, beta, 0)
#                 else:
#                     mov, m = self.minimax(board, cur_mov, depth-1,p1, p2,'maximiser',alpha,beta, 1)
#                 if optimum > m:
#                     optimum = m
#                     opt_mov = cur_mov
#                     beta = min( beta, optimum)
#             else:
#                 _, won = board.update(old_mov, cur_mov, p1)
#                 if won and count!=0:
#                     mov, m = self.minimax(board, cur_mov, depth-1,p1, p2, 'maximiser', alpha, beta, 0)
#                 else:
#                     mov, m = self.minimax(board, cur_mov, depth-1,p1, p2,'minimiser',alpha,beta, 1)
#                 if optimum < m:
#                     optimum = m
#                     opt_mov = cur_mov
#                     alpha = max( alpha, optimum )
#             # board.print_board()
#             # print self.utility(board, p1, p2)
#             # n = raw_input("next?")
#             board.big_boards_status[cur_mov[0]][cur_mov[1]][cur_mov[2]] = '-'
#             board.small_boards_status[cur_mov[0]][cur_mov[1]/3][cur_mov[2]/3] = '-'

#             if  time.time()-self.startTime>self.maxTime:
#                 break

#         return opt_mov, optimum

#     def utility(self,board, p1, p2):
#         win_status = board.find_terminal_state()
#         if  win_status == (p1,'WON'):
#             return 10000000
#         elif win_status == (p2,'WON'):
#             return -10000000
#         elif win_status == ('NONE', 'DRAW'):
#             return 0
        
#         stateGridProbWin = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
#         stateGridProbLose = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
#         stateGridUtilWin = [[[k for k in range(3)] for i in range(3)] for j in range(2)]
#         stateGridUtilLose = [[[k for k in range(3)] for i in range(3)] for j in range(2)]

#         for k in range(2):
#             for i in range(0,9,3):
#                 for j in  range(0,9,3):
#                     a = [board.big_boards_status[k][i+p][j:j+3] for p in range(3)]
#                     hashVal = self.hashSmallBoard(a)
#                     lose,win,den = self.smallBoardUtil[hashVal]
#                     # print type(stateGridProb)
#                     # print i//3
#                     stateGridProbWin[k][i//3][j//3] = float(win)/float(den)
#                     stateGridProbLose[k][i//3][j//3] = float(lose)/float(den)
#                     # print float(num)/float(den)
        
#         for k in range(2):
#             #centre
#             mul = 1
#             stateGridUtilWin[k][1][1] = 0
#             for i in range(3): mul*=stateGridProbWin[k][1][i]
#             stateGridUtilWin[k][1][1] += mul
#             mul = 1
#             for i in range(3): mul*=stateGridProbLose[k][1][i]
#             stateGridUtilLose[k][1][1] += mul            

#             mul = 1
#             for i in range(3): mul*=stateGridProbWin[k][i][1]
#             stateGridUtilWin[k][1][1] += mul
#             mul = 1
#             for i in range(3): mul*=stateGridProbLose[k][i][1]
#             stateGridUtilLose[k][1][1] += mul

#             stateGridUtilWin[k][1][1] += stateGridProbWin[k][0][0]* stateGridProbWin[k][1][1]* stateGridProbWin[k][2][2]
#             stateGridUtilWin[k][1][1] += stateGridProbWin[k][0][2]* stateGridProbWin[k][1][1]* stateGridProbWin[k][2][0]
#             stateGridUtilWin[k][1][1] *= 3

#             stateGridUtilLose[k][1][1] += stateGridProbLose[k][0][0]* stateGridProbLose[k][1][1]* stateGridProbLose[k][2][2]
#             stateGridUtilLose[k][1][1] += stateGridProbLose[k][0][2]* stateGridProbLose[k][1][1]* stateGridProbLose[k][2][0]
#             stateGridUtilLose[k][1][1] *= 3

#             #corner
#             for i in range(3):
#                 for j in range(3):
#                     if j==1 or i==1: continue
#                     mul = 1
#                     stateGridUtilWin[k][i][j] = 0
#                     for p in range(3): mul*=stateGridProbWin[k][i][p]
#                     stateGridUtilWin[k][i][j] += mul

#                     mul = 1
#                     for i in range(3): mul*=stateGridProbWin[k][p][j]
#                     stateGridUtilWin[k][i][j] += mul

#                     stateGridUtilWin[k][i][j] += stateGridProbWin[k][i][j]*stateGridProbWin[k][1][1]* stateGridProbWin[k][2-i][2-j]
#                     stateGridUtilWin[k][i][j] *= 4

#                     mul = 1
#                     stateGridUtilLose[k][i][j] = 0
#                     for p in range(3): mul*=stateGridProbLose[k][i][p]
#                     stateGridUtilLose[k][i][j] += mul

#                     mul = 1
#                     for i in range(3): mul*=stateGridProbLose[k][p][j]
#                     stateGridUtilLose[k][i][j] += mul

#                     stateGridUtilLose[k][i][j] += stateGridProbLose[k][i][j]*stateGridProbLose[k][1][1]* stateGridProbLose[k][2-i][2-j]
#                     stateGridUtilLose[k][i][j] *= 4

            
#             #others
#             for i in range(3):
#                 for j  in range(3):
#                     if i!=1 and j != 1: continue
#                     mul = 1
#                     stateGridUtilWin[k][i][j] = 0
#                     for p in range(3): mul*=stateGridProbWin[k][i][p]
#                     stateGridUtilWin[k][i][j] += mul

#                     mul = 1
#                     for i in range(3): mul*=stateGridProbWin[k][p][j]
#                     stateGridUtilWin[k][i][j] += mul

#                     stateGridUtilWin[k][i][j] *= 6

#                     mul = 1
#                     stateGridUtilLose[k][i][j] = 0
#                     for p in range(3): mul*=stateGridProbLose[k][i][p]
#                     stateGridUtilLose[k][i][j] += mul

#                     mul = 1
#                     for i in range(3): mul*=stateGridProbLose[k][p][j]
#                     stateGridUtilLose[k][i][j] += mul

#                     stateGridUtilLose[k][i][j] *= 6


#         # print stateGridProb[0]
#         # print stateGridProb[1]
#         #take sum of the utilities over the entire board
#         total = 0
#         m1 = 10000000000
#         m2 = -10000000000
#         for k in range(2):
#             for i in range(3):
#                 for j in range(3):
#                     m1 = min(m1, stateGridUtilWin[k][i][j])
#                     m2 = max(m2, stateGridUtilLose[k][i][j])
#                     # total += stateGridUtilWin[k][i][j]
#                     # total -= stateGridUtilLose[k][i][j]

#         total = m1-m2
#         return m2


#     def hashSmallBoard(self,state):
#         hashStr = ''.join([state[i][j] for i in range(3) for j in range(3)])
#         return hashStr

#     # @mem.cache
#     def SmallBoardUtility(self, state, p1, p2, depth):
#         hashStr = self.hashSmallBoard(state)

#         if hashStr in self.smallBoardUtil.keys():
#             return self.smallBoardUtil[hashStr]
                     
#         for i in state:
#             if i == [p1,p1,p1]:
#                 self.smallBoardUtil[hashStr] = (0,1,1)
#                 return (0,1,1)

#         for i in range(3):
#             if [state[j][i] for j in range(3)] == [p1,p1,p1]:
#                 self.smallBoardUtil[hashStr] = (0,1,1)
#                 return (0,1,1)     
        
#         if [state[0][0], state[1][1], state[2][2]] == [p1,p1,p1] or [state[2][0], state[1][1], state[0][2]] == [p1,p1,p1]:
#             self.smallBoardUtil[hashStr] = (0,1,1)
#             return (0,1,1)

#         for i in state:
#             if i == [p2,p2,p2]:
#                 self.smallBoardUtil[hashStr] = (1,0,1)
#                 return (1,0,1)

#         for i in range(3):
#             if [state[j][i] for j in range(3)] == [p2,p2,p2]:
#                 self.smallBoardUtil[hashStr] = (1,0,1)
#                 return (1,0,1)     
        
#         if [state[0][0], state[1][1], state[2][2]] == [p2,p2,p2] or [state[2][0], state[1][1], state[0][2]] == [p2,p2,p2]:
#             self.smallBoardUtil[hashStr] = (1,0,1)
#             return (1,0,1)

#         win = 0
#         lose = 0
#         tot = 0
#         for i in range(3):
#             for j in range(3):
#                 if state[i][j] == '-':
#                     state[i][j] = p1
#                     c,a,b = self.SmallBoardUtility(state, p1, p2, depth+1)
#                     win+=a
#                     lose+=c
#                     tot+=b
#                     state[i][j] = p2
#                     c,a,b = self.SmallBoardUtility(state, p1, p2, depth+1)
#                     win+=a
#                     lose+=c
#                     tot+=b
#                     state[i][j] = '-'

#         if tot == 0:
#             tot = 1
#         self.smallBoardUtil[hashStr] = (lose,win,tot)
#         # print hashStr, (lose,win,tot)
#         # print self.smallBoardUtil['xo-oxoxxo']

#         return (lose,win,tot)
