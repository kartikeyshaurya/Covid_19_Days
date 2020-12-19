from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.
    Go through all the units/squares, and whenever there is a unit with
    a box that contains an unsolved value that only fits in that one box,
    assign the value to this box.
    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in Only Choices.
    """
    logging.info("Only Choice Strategy is processing")

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box
                       for box in unit
                       if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                # PyGame Attempt
                values = assign_value(values, dplaces[0], digit)
    return values

def find_naked_twins(possible_twins, values):
    # Store in list of tuples all pairs of boxes that each contain the same twin possibilities (naked twins)

    logging.info("Naked Twins Strategy - Finding Naked Twins")

    naked_twins = []
    for box_twin1 in possible_twins:
        for box_twin2 in peers[box_twin1]:
            if values[box_twin1] == values[box_twin2]:
                naked_twins.append((box_twin1, box_twin2))
    return naked_twins

def eliminate_twin_values_from_peers(naked_twins, values):
    """
    Iterate over all the pairs of naked twins.
    - Find peer boxes that they have in common between them based on calculating their intersection
    - Iterate over the set of intersecting peers
    - Delete the naked twins values from each of those intersecting peers that contain over two possible values
    """

    logging.info("Naked Twins Strategy - Eliminating Twin Values from from Intersecting Peers")

    for index in range(len(naked_twins)):
        box1, box2 = naked_twins[index][0], naked_twins[index][1]
        peers1, peers2 = peers[box1], peers[box2]
        peers_intersection = set(peers1).intersection(peers2)
        for peer_box in peers_intersection:
            if len(values[peer_box]) > 1:
                for digit in values[box1]:
                    # values[peer_box] = values[peer_box].replace(digit, '')
                    # PyGame Attempt
                    values = assign_value(values, peer_box, values[peer_box].replace(digit,''))
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy. Find all instances of naked twins by:
    - Find all boxes with exactly two possibilities by iterating over all boxes in puzzle.
    - Storing in a list of tuples all pairs of boxes that each contain the same twin possibilities (naked twins)
    - Iterate over all the pairs of naked twins to:
        - Find peer boxes that they have in common between them based on calculating their intersection
        - With the set of intersecting peers determined, iterate over the set of intersecting peers and
        delete the naked twins values from each of those intersecting peers that contain more than two possible values
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    logging.info("Naked Twins Strategy processing")

    # Find all boxes containing exactly two possibilities
    possible_twins = [box
                      for box in values.keys()
                      if len(values[box]) == 2]
    # print("Possible naked twins: ", possible_twins)

    naked_twins = find_naked_twins(possible_twins, values)

    eliminate_twin_values_from_peers(naked_twins, values)

    return values


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    for unit in unitlist:
        for digit in '123456789':
            num_hits = 0;
            for box in unit:
                if digit in values[box]:
                    num_hits= num_hits + 1
                    last_box = box
            if num_hits == 1:
                values[last_box] = digit
    return values



def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values
        
    # If you're stuck, see the solution.py tab!
    minvalue = 10
    for box in boxes:
        if len(values[box]) > 1:
            if len(values[box]) < minvalue:
                minvalue = len(values[box])
                bestbox = box
    for value in values[bestbox]:
        new_sudoku = values.copy()
        new_sudoku[bestbox] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt 


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
