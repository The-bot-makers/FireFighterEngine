import chess as gamelib
import threading
import time
from numba import jit

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
        brd=gamelib.Board()
        brd.set_fen(fen)
        