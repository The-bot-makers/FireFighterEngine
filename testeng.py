import main
eng=main.FFEngine()
thread=2
fen="2k5/8/8/8/8/8/8/2KB4 w - - 0 1"
depth=3
print(eng.GetEvalnumber(fen))