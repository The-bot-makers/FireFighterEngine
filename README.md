# FireFighterEngine : A UCI Chess Engine Written In Python

## How It Works

This is a chess engine written in python, using the convensional brute force method. It analyzes the last node of each branch, then it decides the one which has the most advantage. Next it checks if with a different opponent move, what would be its **[Eval Number](https://github.com/The-bot-makers/FireFighterEngine#Eval-Number)**. Here alpha-beta is involved. If any branch has less than (undecided) advantage, it is cancelled. The advantages are then averaged out.It does the same with each move and then each thread returns a best move. They get added to the 'Qualified Moves' list. Then each 'qualified move' goes through the same process as mentioned above and finally, returns the final best move.

## How To Use It

You need the python package installed for this(coming soon) or the code. Import the package(or the file 'main.py' of the source code) and then create an instance of the class 'FFEngine'. All you need to do to get the move is to call the 'Play' method of the class with the arguments as threads, fen, and depth. It will return the best move.

## Eval Number

The eval number is a number representing how much advantage the engine has. It is calculated as follows:-
  
### Material
  
+1 pawn   = +1 eval number

+1 knight = +3 eval number

+1 bishop = +3 eval number

+1 rook   = +5 eval number

+1 queen  = +9 eval number
  
### Positional
  
Extra pawn on the same file = -(1st extra pawn = -0.1, 2nd = -0.2(total -0.3 because of the 1st) 3rd = -0.3(total -0.6 because of the 1st and 2nd). Then they get added up.)
