import main
eng=main.FFEngine()
thread=2
fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
depth=3
print(eng.Play(thread,fen,depth))
