import chess
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
            brd=currboard
            brd.push(moves[0])
            currbranch=[]
            currbranch.append(0)
            if self.UnusedThreads>0:
                nxtthreadid=threadid
                nxtthreadid.append[0]
                thrdid=0
                pmoves=list(currboard.legal_moves)
                div=int(len(pmoves)/self.UnusedThreads)
                if div<1:
                    self.UnusedThreads-=len(pmoves)
                    for move in pmoves:
                        self.threadlist.append(threading.Thread(target=self.ProcessMove,args=([move],brd,depth-1,nxtthreadid,)))
                        self.threadlist[-1].start()
                        time.sleep(0.8)
                        thrdid+=1
                        nxtthreadid[-1]=thrdid
                else:
                    for i in range(self.UnusedThreads-1):
                        self.threadlist.append(threading.Thread(target=self.ProcessMove,args=(pmoves[div*i:div*(i+1)],brd,depth-1,nxtthreadid,)))
                        self.threadlist[-1].start()
                        time.sleep(0.8)
                        thrdid+=1
                        nxtthreadid[-1]=thrdid
                    self.threadlist.append(threading.Thread(target=self.ProcessMove,args=(pmoves[len(pmoves)-div:len(pmoves)],brd,depth-1,nxtthreadid,)))
                    self.threadlist[-1].start()
                
    def Play(self,threads,fen,depth):
        if fen in self.Premoves:
            return self.Premoves[fen]
        else:
            brd=chess.Board()
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
                        self.threadlist.append(threading.Thread(target=self.ProcessMove,args=([move],brd,depth,[threadid],)))
                        self.threadlist[-1].start()
                        time.sleep(0.8)
                        threadid+=1
                else:
                    for i in range(threads-1):
                        self.threadlist.append(threading.Thread(target=self.ProcessMove,args=(pmoves[div*i:div*(i+1)],brd,depth,[threadid],)))
                        self.threadlist[-1].start()
                        time.sleep(0.8)
                        threadid+=1
                    self.threadlist.append(threading.Thread(target=self.ProcessMove,args=(pmoves[len(pmoves)-div:len(pmoves)],brd,depth,[threadid],)))
                    self.threadlist[-1].start()
                return None