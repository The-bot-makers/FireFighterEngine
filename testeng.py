import main
eng=main.FFEngine()
thread=2
fen="3kr3/8/8/8/8/4PP2/3KBB2/8 b - - 0 1"
depth=3
print(eng.GetEvalnumber(fen))
