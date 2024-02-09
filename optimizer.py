from pulp import *

def get_squares(Players, Squares):
    if sum(Squares) < 100:
        Players.append('WILD')
        Squares.append(100-sum(Squares))
    squares_per_player = {k: v for k, v in zip(Players, Squares)}

    Sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Vals = Players
    Rows = Sequence
    Cols = Sequence
    
    # Define Problem       
    prob = LpProblem("SuperBowl Problem",LpMinimize)

    # Creating a Set of Variables
    choices = LpVariable.dicts("Choice",(Vals,Rows,Cols),0,1,LpInteger)

    # Added arbitrary objective function
    prob += 0, "Arbitrary Objective Function"

    # A constraint ensuring that only one value can be in each square is created
    for r in Rows:
        for c in Cols:
            prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

    # Add constraints enforcing that there can only be minimum number of squares per player in each row or column
    for v in Vals:
        for r in Rows:
            prob += lpSum([choices[v][r][c] for c in Cols]) <= (squares_per_player[v] // 10) + 1, ""
            prob += lpSum([choices[v][r][c] for c in Cols]) >= (squares_per_player[v] // 10), ""
            
        for c in Cols:
            prob += lpSum([choices[v][r][c] for r in Rows]) <= (squares_per_player[v] // 10) + 1, ""
            prob += lpSum([choices[v][r][c] for r in Rows]) >= (squares_per_player[v] // 10), ""

        prob += lpSum([[choices[v][r][c] for r in Rows] for c in Cols]) == squares_per_player[v], ""
                

    # Add constraints to minimize total duplicates in rows and columns
    prob += lpSum([[[choices[v][r][c] + choices[v][r][c2] for c in Cols for c2 in Cols if c != c2] for r in Rows] for v in Vals])  # Minimize duplicates in rows
    prob += lpSum([[[choices[v][r][c] + choices[v][r2][c] for r in Rows for r2 in Rows if r != r2] for c in Cols] for v in Vals])  # Minimize duplicates in columns

    # Add constraints to minimize total duplicates in rows and columns for each name
    for v in Vals:
        for r in Rows:
            prob += lpSum([choices[v][r][c1] + choices[v][r][c2] for c1 in Cols for c2 in Cols if c1 != c2])

        for c in Cols:
            prob += lpSum([choices[v][r1][c] + choices[v][r2][c] for r1 in Rows for r2 in Rows if r1 != r2])

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    print("Status:", LpStatus[prob.status])

    # Print out the solution
    print("\nSuper Bowl Squares Solution")
    if LpStatus[prob.status] == 'Optimal':
        matrix = []
        for r in Rows:
            row = []
            for c in Cols:
                for v in Vals:
                    if choices[v][r][c].varValue == 1:   
                        row.append(v)            
            matrix.append(row)
    else:
        print('Problem is infeasible')

    return matrix