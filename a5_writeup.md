# Assignment 5 Write up

Assignment 5 can be broken up into the following parts:
1. Import the Necessary Modules:
- `copy`: For creating deep copies of objects
- `Stack` and `Queue`: Custom implementations for DFS and BFS operations
2. Utility Functions: 
- `remove_if_exists`: Removes a specified element from a list if it exists, which is used to remove the possibilites from a cell
3. Board Class:
- Represents the Sudoku board
- Consists of functions that will find the most constrained cell, and update the board, which eliminates possible solutions
4. DFS & BFS Functions:
- `DFS`: Uses depth-first search to solve the Sudoku puzzle. It works by trying to fill the most constrained cell with potential values until a solution is found or backtracks if a mistake is made
- `BFS`: Uses breadth-first search to solve the Sudoku puzzle in a similar fashion to DFS but explores nodes level by level
5. Main Execution:
- Defines two different sets of initial moves for Sudoku puzzles
- Uses both DFS and BFS to solve each puzzle and prints the results


After completing the assignment, answer the following reflection questions:

## Reflection Questions

1. How do the performance and efficiency of the Depth-First Search (DFS) and Breadth-First Search (BFS) algorithms compare when solving Sudoku puzzles? In what scenarios might one approach be preferable over the other?
DFS is generally faster and more efficient for solving Sudoku puzzles because it had the ability to explore as far as possible along each branch before backtracking. This approach is more helpful in Sudoku, where the most constrained cells are often the ones needed to be solved first. while, BFS explores all options at the current depth level before moving on to options at the next depth level, which can lead to a higher number of iterations and being slower overall. BFS might be preferable in scenarios where the most constrained cell isn't findable?


2. How did the choice of data structures (like the Stack for DFS and Queue for BFS) impact the implementation and functionality of the algorithms? Are there alternative data structures or design patterns that could have been used to achieve the same objectives?
The Stack made it possible to go back in DFS, enabling the program to return to previous states when a dead end was reached, and was overall better. The Queue, in general took longer and didnt seem to have an upside.


3. Considering the current implementation, how might the Sudoku solver be adapted or extended for larger puzzles or different types of grid-based logic games? How can the lessons learned from this assignment be applied to real-world problem-solving or optimization challenges?
To work with larger puzzles you would have to have to make the board larger and update any other functions that are restricted to the 9x9 board. for other logic games you could keep the DFS and BFS functions possibly modifiying them a little. You can take ideas from depth search and breath search to apply when solving problems yourself in the real world.