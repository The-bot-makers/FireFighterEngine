import tensorflow as tf
import numpy as np
import chess

#load the saved model
model=tf.keras.models.load_model('openlock_model')

#rest explained in nntest.py
probmodel=tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])


PieceNum={'p':'0','n':'1','b':'2','r':'3','q':'4','k':'5','.':'6'}


def numreprgen(repres):
    splted=[repres[0:8],repres[8:16],repres[16:24],repres[24:32],repres[32:40],repres[40:48],repres[48:56],repres[56:64]]  
    numsplted=[]
    for j in splted:
        toappend=[]
        for k in j:
            toappend.append(PieceNum[k.lower()])
        numsplted.append(toappend)
    for j in range(len(numsplted)):
        for k in range(8):
            numsplted[j][k]=int(numsplted[j][k])/6.0
    return numsplted
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


testfen='r4r1k/p5p1/1pRq2np/5p2/7P/P4BP1/1P2QP2/2K1R3 b - - 0 1'


probs=probmodel(np.array([numreprgen(reprgener(testfen))]))


print(np.argmax(probs))
print(probs)