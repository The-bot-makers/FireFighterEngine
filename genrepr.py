import chess
from chess import svg
import pandas as pd
doc=pd.read_excel('NeuralNNTf.xlsx',sheet_name='LockedPos')
del doc['Unnamed: 0']
cpgn=open('cpgn.txt')
cpgn=cpgn.readlines()
ecpgn=cpgn.copy()
ind=0

def reprgener(fen):
    brd=chess.Board()
    brd.set_fen(fen)
    bb=chess.BaseBoard()
    bb.set_board_fen(brd.board_fen())
    pcmap=bb.piece_map()
    repres=[]
    for i in range(64):
        if i in pcmap:
            repres.append(pcmap[i].symbol())
        else:
            repres.append('.')
    strrepres=''.join([elem for elem in repres])
    return strrepres


for line in cpgn:
    if ind%90==0:
        fen=line.split(' ')[1]
        representation=reprgener(fen)
        with open('board.svg','w') as svgbrd:
            svgbrd.write(svg.board(chess.Board(fen)))
        locked=int(input('Locked?'))
        doc=doc.append(pd.DataFrame([[representation,fen,locked]],columns=['Repr','Fen','Locked']))
        doc.index=[ind for ind in range(len(doc.axes[0]))]
        doc.to_excel('NeuralNNTf.xlsx',sheet_name='LockedPos')
        with open('checkpoint.txt','w') as newcpgn:
            newcpgn.write(''.join(map(str,ecpgn)))
    del ecpgn[0]
    ind+=1
    
