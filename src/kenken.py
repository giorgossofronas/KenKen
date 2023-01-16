import csp
import sys

class KenKen(csp.CSP):
    """This class inherits from the CSP class, from AIMA book,
    to solve KenKen puzzles of all sizes and difficulties.
    """
    def __init__(self, size: int, grid: tuple):
        """Initializes a new KenKen puzzle and its variables, domains, neighbors, and constraint function.
        
        Parameters:
            size: The size of the KenKen puzzle, a square puzzle with dimensions size x size.
            grid: A tuple of strings representing the cages and their goal numbers and operations.
                Each string should be in the following format: 
                    '[(row,col),(row,col)]<operation><goal>'
                For example, a cage containing cells (1, 1) and (1, 2) with a goal of 3 and an operation of addition
                would be represented as: '[(1,1),(1,2)]+3'
        
        Attributes:
            size: The size of the KenKen puzzle, a square puzzle with dimensions size x size.
            constraint_checks: The number of constraint checks performed during the solving process.
            cages: A dictionary mapping each cage's cells to a tuple containing the operation and goal number
                for the cage.
            operations: A dictionary mapping operations to their corresponding lambda functions.
        """
        self.size = size
        self.constraint_checks = 0

        variables = tuple(v for v in range(1, self.size ** 2 + 1))

        domains = {var: tuple(range(1, self.size + 1)) for var in variables}

        self.cages = {}
        for cage in grid:
            curr_cage = []
            for i, char in enumerate(cage):
                if char == '(':
                    row, col = map(int, cage[i+1:i+4:2])
                    # convert (row, col) -> value | ex. 3x3 puzzle: (3, 1) -> 7
                    val = (row - 1) * self.size + col
                    curr_cage.append(val)
                elif char == ']':
                    op = cage[i+1]
                    goal = int(''.join(cage[i+2:]))
                    self.cages[tuple(curr_cage)] = (op, goal)
                    break

        neighbors = {}
        for var in variables:
            # init neighbors that (may) participate in constraints
            neighbors_list = []

            # var's cage
            cage_var, _ = self.find_cage(var)

            for v in variables:
                # same row or col or cage
                if var != v and (self.same_row_or_col(var, v) or v in cage_var):
                    neighbors_list.append(v)

            neighbors[var] = tuple(neighbors_list)

        self.operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: abs(x - y),
            '*': lambda x, y: x * y,
            '/': lambda x, y: max(x, y) / min(x, y)
        }

        super().__init__(
            variables,
            domains,
            neighbors,
            self.kenken_constraint
        )

    def same_row_or_col(self, A, B) -> bool:
        """Returns True if cells A and B are in the same row or column, False otherwise."""
        if ((A-1) // self.size == (B-1) // self.size or 
            (A-1) % self.size == (B-1) % self.size):
            return True

    def find_cage(self, A, B=None) -> tuple:
        """Returns a tuple of the cages containing cell A and cell B.
        If B is not provided, returns only the cage of cell A.
        """
        cageA = cageB = None
        for c in self.cages:
            if A in c:
                cageA = c
                if not B:
                    break
            if B in c:
                cageB = c
            if cageA and cageB:
                break
        return (cageA, cageB)

    def kenken_constraint(self, A, a, B, b) -> bool:
        """Returns True if the assignment of value a to cell A and
        value b to cell B does not violate any KenKen constraints, False otherwise.
        """
        self.constraint_checks += 1
        
        # same row or col and equal
        if a == b and self.same_row_or_col(A, B):
            return False
        
        cageA, cageB = self.find_cage(A, B)
        if cageA == cageB:
            return self.cage_constraint(cageA, A, a, B, b)
        else:
            # if not in same cage check for constraints in each cell's cage separately
            return self.cage_constraint(cageA, A, a) and self.cage_constraint(cageB, B, b)

    def cage_constraint(self, cage, A, a, B=None, b=None) -> bool:
        """Returns True if the constraints of given cage are being satisfied, False otherwise.
        If both cells A, B are provided we suppose that they are in the same cage, else not.
        """
        op, goal = self.cages[cage]

        if op == 'N':
            return a == goal
        elif op in {'-', '/'}:
            try:
                return self.operations[op](a, b) == goal
            except TypeError:
                other_var = (set(cage) - {A}).pop()
                if other_var in self.infer_assignment():
                    return self.operations[op](a, self.infer_assignment()[other_var]) == goal
                else:
                    # check if there is a choice/value that can lead to cage constraint satisfaction
                    return any(self.operations[op](a, c) == goal for c in self.choices(other_var))
        
        # init result variable depending on operation
        result = 0 if op == '+' else 1

        # non-yet assigned members
        non_assigned = set()
        for m in cage:
            element = a if m == A else b if m == B else self.infer_assignment().get(m)
            if element is None:
                non_assigned.add(m)
                continue
            result = self.operations[op](result, element)
            
        # check if values to all cage members have been assigned
        left = len(non_assigned)
        if left == 0:
            return result == goal
        elif left == 1:
            other_var = non_assigned.pop()
            # check if there is a choice/value that can lead to cage constraint satisfaction
            return any(self.operations[op](result, c) == goal for c in self.choices(other_var))
        else:
            return result + left <= goal if op == '+' else result <= goal
    
    def solve(self, algorithm) -> dict:
        """Solves the KenKen puzzle using the prefered CSP solving algorithm.
        Note that AIMA's implementation of MRV resolves ties randomly, so the 
        number of assignments made may vary each time.
        """
        if algorithm == 'BT':
            return csp.backtracking_search(self)
        elif algorithm == 'BT-MRV':
            return csp.backtracking_search(self, select_unassigned_variable=csp.mrv)
        elif algorithm == 'FC':
            return csp.backtracking_search(self, inference=csp.forward_checking)
        elif algorithm == 'FC-MRV':
            return csp.backtracking_search(self, inference=csp.forward_checking, select_unassigned_variable=csp.mrv)
        elif algorithm == 'MAC':
            return csp.backtracking_search(self, inference=csp.mac)
        else:
            raise ValueError(f'Invalid input: {algorithm} is not one of the offered algorithms.')
    
    def display(self, assignment: dict):
        """Displays a KenKen puzzle."""
        print('+' + '-' * (self.size * 4 - 1) + '+')
        for cell in self.variables:
            try:
                print('|', assignment[cell], end=' ')
            except Exception:
                print('| [ERROR]: value not in dict. ', end='')

            # start a new line
            if cell % self.size == 0:
                print('|')
                print('+' + '-' * (self.size * 4 - 1) + '+')
        print()
        
    
def parse_input() -> tuple:
    """Reads a KenKen puzzle from a file and returns its size, grid, and chosen algorithm.
    The first command line argument should be the name of the file containing the puzzle, without the '.txt' extension
    and the second argument should be the desired algorithm to use. The file should be placed in the 'test_cases/' folder
    and have a '.txt' extension. For example, for a file called '5x5.txt' and algorithm=MAC, the command would be:
    python solve.py 5x5 MAC
    """
    if len(sys.argv) != 3:
        raise ValueError('Invalid input, proper format is: python solve.py <file name> <algorithm>')

    file_name = '../test_cases/' + sys.argv[1] + '.txt'
    algorithm = sys.argv[2]

    # open puzzle file
    # first line is size (ex. 4 for 4x4 puzzle) and other lines are the cages
    with open(file_name, 'r') as file:
        puzzle = [i.strip() for i in file.readlines()]
    
    return (int(puzzle.pop(0)), tuple(puzzle), algorithm)