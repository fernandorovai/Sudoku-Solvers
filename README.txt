You can run the program just running the file AC3.py.
As a conventional call: python AC3.py

The file testRead.py contains the parser and is required to run the program.
You can choose the puzzle just setting a different number in a variable puzzle. 
(puzzle = puzzles[2], for example, will use the 3rd puzzle from the testSudoku.txt)
The variable is located in AC3.py, in the method tryAC3() - line 190.

It is possible to add more puzzles using the file testSudoku.txt
NOTE: I hard-coded the search technique in the AC3.py file.
You can choose the search technique to solve the problem. (Breath-First Search or Depth-First Search)
      inside the method tryAC3() - line 228. (searchTechnique = "DFS";) or (searchTechnique = "BFS";)
