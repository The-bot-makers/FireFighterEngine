import tensorflow as tf
import pandas as pd
import numpy as np
import chess

#opening the dataset
doc=pd.read_excel('NeuralNNTf.xlsx',sheet_name='LockedPos')
del doc['Unnamed: 0']

#getting the columns
reprs=list(doc['Repr'])
Locks=list(doc['Locked'])

#to convert the representation into numbers
PieceNum={'p':'0','n':'1','b':'2','r':'3','q':'4','k':'5','.':'6'}

#training arrays
x_train=[]
y_train=[]

#converting the representation into tensorflow readable array
for i in reprs:
    splted=[i[0:8],i[8:16],i[16:24],i[24:32],i[32:40],i[40:48],i[48:56],i[56:64]]
    numsplted=[]
    for j in splted:
        toappend=[]
        for k in j:
            toappend.append(PieceNum[k.lower()])
        numsplted.append(toappend)
    for j in range(len(numsplted)):
        for k in range(8):
            numsplted[j][k]=int(numsplted[j][k])/6.0
    x_train.append(numsplted)
    
#adding 2 so that values start from 0 instead of -2       
for i in range(len(Locks)):
    Locks[i]=Locks[i]+2
    
#converting lists into arrays
x_train=np.array(x_train)
y_train=np.array(Locks)

#to create a hidden layer(line of neurons)
def CreateLayer(Neurons,Activation):
    return tf.keras.layers.Dense(Neurons,activation=Activation)

#creating the model with: input neurons(tf.keras.layers.Flatten(input_shape=(8, 8))), 3 hidden layers, 5 output neurons(tf.keras.layers.Dense(5))
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(8, 8)),
  CreateLayer(128, 'relu'),
  CreateLayer(128, 'relu'),
  CreateLayer(128, 'relu'),
  tf.keras.layers.Dense(5)
])

#getting the model ready for training by setting the compilation options: optimizer(idk), loss function to 'direct' the training, and the metrics to display while training
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#training the model, once the dataset gets huge, a batch size will be added so that the computer memory can handle it
model.fit(x_train, y_train, epochs=200)

#creating the probability model which makes predictions
probmodel=tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

#converting representations into tf readable input data(same as the one given as the training input)
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

#fen2representation
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

#make prediction
print(np.argmax(probmodel(np.array([numreprgen(reprgener('2k2b2/7P/8/8/8/2K1NB1p/6N1/8 w - - 0 1'))]))[0]))

#save the model
model.save('openlock_model')