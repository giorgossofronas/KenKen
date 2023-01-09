# KenKen Solver

A Python project that implements an efficient solver for KenKen puzzles using Constraint Satisfaction Problems (CSP) algorithms from the book Artificial Intelligence: A Modern Approach (AIMA). The project was developed in Python 3.7

[KenKen](https://en.wikipedia.org/wiki/KenKen) is a mathematical puzzle that requires players to fill in a grid with numbers while satisfying the following constraints:
- Numbers should be in the range of 1 to N, where NxN is the puzzle's size.<br>
- Each row and column contains a unique set of numbers, meaning that the same number can't be repeated in the same row or column.<br>
- The top left corner of each cage has a "target number" and a math operation. The numbers you enter into a cage must combine (in any order) to produce the target number using the noted operation. If no operation is mentioned then the cage only has one cell/member and its value should be equal to the target number.

## How does the solver work?
The solver gives the user the option to choose from a variety of search algorithms. The algorithms of interest for this project are:
- [Backtracking (BT)](https://ktiml.mff.cuni.cz/~bartak/constraints/propagation.html#BT)
- [Forward Checking (FC)](https://ktiml.mff.cuni.cz/~bartak/constraints/propagation.html#FC)
- [Maintaining Arc Consistency (MAC)](https://ktiml.mff.cuni.cz/~bartak/constraints/propagation.html#LA)

There is also the option to use the [Minimum Remaining Values (MRV)](https://cs188ai.fandom.com/wiki/Minimum_Remaining_Values) heuristic with Backtracking and Forward Checking (**BT-MRV** and **FC-MRV**).<br>

## How do I use the solver?
The input puzzle files should be formatted as follows:
```
    <puzzle size>
    [(row,col),(row,col)]<operation><target number>
    ...
    [(row,col),(row,col)]<operation><target number>
```
For instance, the puzzle size is 4 for a 4x4 puzzle. Each following line represents the cages with their members' coordinates in (row,col) format, starting from (1,1) to (N, N). You can find full examples in the [`test_cases/`](https://github.com/giorgossofronas/kenken/tree/main/test_cases) folder, in which there are plenty of **hard** KenKen puzzles from [kenkenpuzzle.com](http://www.kenkenpuzzle.com/).
<br><br>
To run the solver, select or place a new puzzle-file in the `test_cases/` folder and make sure that it has a `.txt` extension. After that, simply execute the command:
```bash
    python solve.py <file name> <algorithm>
```
For example, for a file called "8x8.txt" and wanted algorithm being Forward Checking the command would be: `python solve.py 8x8 FC`<br>

## References
* [Artificial Intelligence: A Modern Approach (AIMA)](https://github.com/aimacode/aima-python)<br>
* [kenkenpuzzle.com](http://www.kenkenpuzzle.com/)

 ---
 © Giorgos Sofronas
