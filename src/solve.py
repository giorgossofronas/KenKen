from kenken import *
from time import perf_counter

def main():
    """Example of how to use the KenKen solver."""
    
    # init puzzle based on provided input
    size, grid, algorithm = parse_input()
    puzzle = KenKen(size, grid)

    print(f'\nPuzzle size: {size}x{size}')
    print(f'Algorithm used: {algorithm}')
    print('\nSolution:')

    # solve puzzle and calculate elapsed time
    dt = perf_counter()
    solution = puzzle.solve(algorithm)
    dt = perf_counter() - dt
    
    # print solution
    puzzle.display(solution)

    # stats
    print(f'Assignments: {puzzle.nassigns}')
    print(f'Constraints checks: {puzzle.constraint_checks}')
    print(f'Time: {dt:.3f} seconds')

if __name__ == '__main__':
    main()