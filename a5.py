import copy  # to make a deepcopy of the board
from typing import List, Any, Tuple

# import Stack and Queue classes for BFS/DFS
from stack_and_queue import Stack, Queue

# HELPER FUNCTION TO REMOVE ITEMS FROM A LIST
def remove_if_exists(lst: Any, elem: Any) -> None:
    """Takes a list and element and removes that element if it exists in the list

    Args:
        lst - the list you're trying to remove an item from
        elem - item to remove
    """
    if isinstance(lst, list) and elem in lst:
        lst.remove(elem)


# NOTE: The linter will complain at you due to the code using member variables like row,
# num_nums_placed & size since you haven't added those in the constructor. Implement the
# constructor before worrying about these errors (if they're still there after you've
# implemented the constructor that's probably a sign your constructor has a bug in it)
class Board:
    """Represents a state (situation) in a Sudoku puzzle. Some cells may have filled in
    numbers while others have not. Cells that have not been filled in hold the potential
    values that could be assigned to the cell (i.e. have not been ruled out from the
    row, column or subgrid)

    Attributes:
        num_nums_placed - number of numbers placed so far (initially 0)
        size - the size of the board (this will always be 9, but is convenient to have
            an attribute for this for debugging purposes)
        rows - a list of 9 lists, each with 9 elements (imagine a 9x9 sudoku board).
            Each element will itself be a list of the numbers that remain possible to
            assign in that square. Initially, each element will contain a list of the
            numbers 1 through 9 (so a triply nested 9x9x9 list to start) as all numbers
            are possible when no assignments have been made. When an assignment is made
            this innermost element won't be a list of possibilities anymore but the
            single number that is the assignment.
    """

    def __init__(self):
        """Constructor for a board, sets up a board with each element having all
        numbers as possibilities"""
        self.size: int = 9
        self.num_nums_placed: int = 0

        # triply nested lists, representing a 9x9 sudoku board
        # 9 quadrants, 9 cells in each 3*3 subgrid, 9 possible numbers in each cell
        # Note: using Any in the type hint since the cell can be either a list (when it
        # has not yet been assigned a value) or a value (once it has been assigned)
        # Note II: a lone underscore is a common convention for unused variables
        self.rows: List[List[Any]] = (
            [[list(range(1, 10)) for _ in range(self.size)] for _ in range(self.size)]
        )

    def __str__(self) -> str:
        """String representation of the board"""
        row_str = ""
        row_num = 0
        for r in self.rows:
            row_str += f"Row {row_num}: {r}\n"
            row_num += 1

        return f"num_nums_placed: {self.num_nums_placed}\nboard (rows): \n{row_str}"

    def print_pretty(self):
        board_str = ""
        for i, row in enumerate(self.rows):
            if i % 3 == 0:
                board_str += " -------------------------\n"
            for j, cell in enumerate(row):
                if j % 3 == 0:
                    board_str += " |"
                board_str += f" {cell if isinstance(cell, int) else '.'}"
            board_str += " |\n"
        board_str += " -------------------------\n"
        print(board_str)


    def subgrid_coordinates(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all coordinates of cells in a given cell's subgrid (3x3 space)

        Integer divide to get column & row indices of subgrid then take all combinations
        of cell indices with the row/column indices from those subgrids (also known as
        the outer or Cartesian product)

        Args:
            row - index of the cell's row, 0 - 8
            col - index of the cell's col, 0 - 8

        Returns:
            list of (row, col) that represent all cells in the box.
        """
        subgrids = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
        # Note: row // 3 gives the index of the subgrid for the row index, this is one
        # of 0, 1 or 2, col // 3 gives us the same for the column
        return [(r, c) for c in subgrids[col // 3] for r in subgrids[row // 3]]

    def find_most_constrained_cell(self) -> Tuple[int, int]:
        """Finds the coordinates (row and column indices) of the cell that contains the
        fewest possible values to assign (the shortest list). Note: in the case of ties
        return the coordinates of the first minimum size cell found

        Returns:
            a tuple of row, column index identifying the most constrained cell
        """
        mini = 9
        row = 0
        column = 0
        for i, col in enumerate(self.rows):
            for j , cell in enumerate(col):
                if isinstance(cell, list) and len(cell) < mini:
                    mini = len(cell)
                    row = i
                    column = j
        return (row, column)

    def failure_test(self) -> bool:
        """Check if we've failed to correctly fill out the puzzle. If we find a cell
        that contains an [], then we have no more possibilities for the cell but haven't
        assigned it a value so fail.

        Returns:
            True if we have failed to fill out the puzzle, False otherwise
        """
        for row in self.rows:
            for col in row:
                if col == []:
                    return True
                
        return False

    def goal_test(self) -> bool:
        """Check if we've completed the puzzle (if we've placed all the numbers).
        Naively checks that we've placed as many numbers as cells on the board

        Returns:
            True if we've placed all numbers, False otherwise
        """
        return self.num_nums_placed == self.size*self.size

    def update(self, row: int, column: int, assignment: int) -> None:
        """Assigns the given value to the cell given by passed in row and column
        coordinates. By assigning we mean set the cell to the value so instead the cell
        being a list of possibities it's just the new assignment value.  Update all
        affected cells (row, column & subgrid) to remove the possibility of assigning
        the given value.

        Args:
            row - index of the row to assign
            column - index of the column to assign
            assignment - value to place at given row, column coordinate
        """
        self.rows[row][column] = assignment
        self.num_nums_placed += 1

        for i in range(self.size):
            remove_if_exists(self.rows[row][i], assignment)
            remove_if_exists(self.rows[i][column], assignment)

        for i, j in self.subgrid_coordinates(row, column):
            remove_if_exists(self.rows[i][j], assignment)





def DFS(state: Board) -> Board:
    s = Stack([state])
    num = 0

    while not s.is_empty():
        b: Board = s.pop()
        num += 1
        if b.goal_test():
            print(f"Number of Iterations: {num}")
            return b
        mcc = b.find_most_constrained_cell()
        row, col = mcc
        for sel in b.rows[row][col]:
            cpy = copy.deepcopy(b)
            cpy.update(row, col, sel)
            s.push(cpy)
    return None  # Return None if no solution is found


def BFS(state: Board) -> Board:
    q = Queue([state])
    num = 0

    while not q.is_empty():
        b: Board = q.pop()
        num += 1
        if b.goal_test():
            print(f"Number of Iterations: {num}")
            return b
        mcc = b.find_most_constrained_cell()
        row, col = mcc
        for sel in b.rows[row][col]:
            cpy = copy.deepcopy(b)
            cpy.update(row, col, sel)
            q.push(cpy)
    return None 



if __name__ == "__main__":
   
    b = Board()
    print(b)
    b.print_pretty()
    b.update(0, 0, 1)
    b.update(0, 2, 2)
    b.update(1, 0, 9)
    b.update(1, 1, 8)
    b.update(0, 4, 3)
    b.update(1, 3, 2)
    b.update(1,6, 4)
    b.update(1, 8, 3)
    print(b)
    b.print_pretty()

    # CODE BELOW HERE RUNS YOUR BFS/DFS
    print("<<<<<<<<<<<<<< Solving Sudoku >>>>>>>>>>>>>>")

    def test_dfs_or_bfs(use_dfs: bool, moves: List[Tuple[int, int, int]]) -> None:
        b = Board()
        # make initial moves to set up board
        for move in moves:
            b.update(*move)

        # print initial board
        print("<<<<< Initial Board >>>>>")
        b.print_pretty()
        # solve board
        solution = (DFS if use_dfs else BFS)(b)
        # print solved board
        print("<<<<< Solved Board >>>>>")
        solution.print_pretty()

    # sets of moves for the different games
    first_moves = [
        (0, 0, 3),
        (0, 4, 8),
        (0, 6, 9),
        (1, 3, 3),
        (1, 4, 4),
        (2, 2, 8),
        (2, 5, 5),
        (2, 6, 6),
        (3, 0, 5),
        (3, 3, 1),
        (3, 5, 4),
        (3, 7, 7),
        (4, 2, 2),
        (4, 5, 9),
        (4, 7, 1),
        (5, 2, 3),
        (5, 7, 4),
        (6, 2, 5),
        (6, 5, 1),
        (6, 6, 2),
        (8, 1, 7),
        (8, 5, 8),
        (8, 7, 9),
    ]

    b = Board()
    #Place the 28 assignments in first_moves on the board.
    for trip in first_moves:
        b.rows[trip[0]][trip[1]] = trip[2]
    #NOTE - the above code only *puts* the numbers on the board, but doesn't
    #   do the work that update does (remove numbers from other lists, etc).

    #I'm going to now alter 3 lists on the board to make them shorter (more
    #   constrained. 
    remove_if_exists(b.rows[0][0], 8)
    remove_if_exists(b.rows[0][0], 7)
    remove_if_exists(b.rows[0][0], 3)
    remove_if_exists(b.rows[0][0], 2)
    remove_if_exists(b.rows[4][8], 8)
    remove_if_exists(b.rows[4][8], 1)
    remove_if_exists(b.rows[4][8], 2)
    remove_if_exists(b.rows[4][8], 3)
    remove_if_exists(b.rows[4][8], 4)
    remove_if_exists(b.rows[6][7], 2)
    remove_if_exists(b.rows[6][7], 3)
    remove_if_exists(b.rows[6][7], 5)
    remove_if_exists(b.rows[6][7], 6)
   
def test_dfs_or_bfs(use_dfs: bool, moves: List[Tuple[int, int, int]]) -> None:
    b = Board()
    # Make initial moves to set up the board
    for move in moves:
        b.update(*move)

    # Print the initial board
    print("<<<<< Initial Board >>>>>")
    b.print_pretty()

    # Solve the board
    solution = (DFS if use_dfs else BFS)(b)

    # Check if a solution was found
    if solution:
        print("<<<<< Solved Board >>>>>")
        solution.print_pretty()
    else:
        print("No solution found.")

print("Using DFS")
test_dfs_or_bfs(use_dfs=True, moves=first_moves)

print("\nUsing BFS")
test_dfs_or_bfs(use_dfs=False, moves=first_moves)