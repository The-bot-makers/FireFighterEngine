import chess as gamelib
import threading
import time

class FFEngine():
    def __init__(self):
        self.QualifiedMoves=[]
        self.Premoves={}
        self.UnusedThreads=0
        self.ThreadList=[]

    def ProcessMove(self,moves,currboard,depth,threadid):
        for move in moves:
            brd=currboard.copy()
            brd.push(move)
            currbranch=[]
            currbranch.append(0)
            if self.UnusedThreads>0:
                nxtthreadid=threadid
                nxtthreadid.append(0)
                thrdid=0
                pmoves=list(currboard.legal_moves)
                div=int(len(pmoves)/self.UnusedThreads)
                if div<1:
                    self.UnusedThreads-=len(pmoves)
                    for move in pmoves:
                        self.ThreadList.append(threading.Thread(target=self.ProcessMove,args=([move],brd,depth-1,nxtthreadid,)))
                        self.ThreadList[-1].start()
                        time.sleep(0.8)
                        thrdid+=1
                        nxtthreadid[-1]=thrdid
                else:
                    for i in range(self.UnusedThreads-1):
                        self.ThreadList.append(threading.Thread(target=self.ProcessMove,args=(pmoves[div*i:div*(i+1)],brd,depth-1,nxtthreadid,)))
                        self.ThreadList[-1].start()
                        time.sleep(0.8)
                        thrdid+=1
                        nxtthreadid[-1]=thrdid
                    self.ThreadList.append(threading.Thread(target=self.ProcessMove,args=(pmoves[len(pmoves)-div:len(pmoves)],brd,depth-1,nxtthreadid,)))
                    self.ThreadList[-1].start()
                    
    def Play(self,threads,fen,depth):
        if fen in self.Premoves:
            return self.Premoves[fen]
        else:
            brd=gamelib.Board()
            brd.set_fen(fen)
            pmoves=list(brd.legal_moves)
            if len(pmoves)==1:
                return pmoves[0].uci()
            else:
                threadid=0
                self.UnusedThreads=threads
                div=int(len(pmoves)/threads)
                if div<1:
                    self.UnusedThreads-=len(pmoves)
                    for move in pmoves:
                        self.ThreadList.append(threading.Thread(target=self.ProcessMove,args=([move],brd,depth,[threadid],)))
                        self.ThreadList[-1].start()
                        time.sleep(0.8)
                        threadid+=1
                else:
                    self.UnusedThreads=0
                    for i in range(threads-1):
                        self.ThreadList.append(threading.Thread(target=self.ProcessMove,args=(pmoves[div*i:div*(i+1)],brd,depth,[threadid],)))
                        self.ThreadList[-1].start()
                        time.sleep(0.8)
                        threadid+=1
                    self.ThreadList.append(threading.Thread(target=self.ProcessMove,args=(pmoves[len(pmoves)-div:len(pmoves)],brd,depth,[threadid],)))
                    self.ThreadList[-1].start()
                return None

    def PonderFixedDepth(self,threads,fen,depth):
        brd=gamelib.Board()
        brd.set_fen(fen)
        
    def PonderInf(self,threads,fen):
        brd=gamelib.Board()
        brd.set_fen(fen)
        
    def GetEvalnumber(self,fen):
        evlnum=0.0
        brd=gamelib.Board()
        brd.set_fen(fen)
        trn=brd.turn
        bb=gamelib.BaseBoard()
        bb.set_board_fen(brd.board_fen())
        piecemap=bb.piece_map()
        engpieces=[x.symbol().lower() for x in list(piecemap.values()) if x.color==trn]
        opppieces=[x.symbol().lower() for x in list(piecemap.values()) if x.color!=trn]
        engadv=engpieces.copy()
        oppadv=opppieces.copy()
        for i in engpieces:
            if i in oppadv:
                engadv.remove(i)
                oppadv.remove(i)
                
        for i in engadv:
            if i=='q':
                evlnum+=9.0
            elif i=='r':
                evlnum+=5.0
            elif i=='b' or i=='n':
                evlnum+=3.0
            elif i=='p':
                evlnum+=1.0
                
        for i in oppadv:
            if i=='q':
                evlnum-=9.0
            elif i=='r':
                evlnum-=5.0
            elif i=='b' or i=='n':
                evlnum-=3.0
            elif i=='p':
                evlnum-=1.0
                
        for i in range(1,9):
            pawns=0
            for j in range(i,64,8):
                if j in piecemap and piecemap[j]==gamelib.Piece(1,trn):
                    pawns+=1
            for j in range(pawns):
                evlnum-=((j+1)/10)
        return evlnum
    def IsLocked(self,fen,pc=10,sqs=gamelib.SquareSet([gamelib.C3,gamelib.C4,gamelib.C5,gamelib.C6,gamelib.D3,gamelib.D4,gamelib.D5,gamelib.D6,gamelib.E3,gamelib.E4,gamelib.E5,gamelib.E6,gamelib.F3,gamelib.F4,gamelib.F5,gamelib.F6,gamelib.B3,gamelib.B4,gamelib.B5,gamelib.B6,gamelib.G3,gamelib.G4,gamelib.G5,gamelib.G6])):
        DetectionRange=sqs
        PieceThreshold=pc
        DetectedPieces=0
        fenbrd=gamelib.Board()
        fenbrd.set_fen(fen)
        bb=gamelib.BaseBoard()
        bb.set_board_fen(fenbrd.board_fen())
        del(fenbrd)
        pcs=list(bb.piece_map().keys())
        for sqr in DetectionRange:
            if sqr in pcs:
                DetectedPieces+=1
        if DetectedPieces>PieceThreshold:
            return True
        else:
            return False