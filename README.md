# FireFighterEngine : A Chess Engine In Python
<br>

## How It Works

This is a chess engine written in python, using the convensional brute force method. It analyzes the last node of each branch, then it decides the one which has the most advantage. Next it checks if with a different opponent move, what would be its advantage. It does the same with each move and then each thread returns a best move. They get added to the 'Qualified Moves' list. Then each 'qualified move' goes through the same process as mentioned above and finally, returns the final best move.
<br>

## How To Use It

You need the python package installed for this(coming soon) or the code. Import the package(or the file 'main.py' of the source code) and then create an instance of the class 'FFEngine'. All you need to do to get the move is to call the 'Play' method of the class with the arguments as threads, fen, and depth. It will return the best move.
