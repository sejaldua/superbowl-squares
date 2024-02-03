from pulp import *

matrix =  [[""]*10]*10
print(matrix)

# print sudoku problem
for row in matrix:
    for i, cell in enumerate(row):
        if i < len(row) - 1:
            print(cell, end=" ")
        else:
            print(cell)
    print()
print("+-------+-------+-------+")

Players = [chr(65+i) for i in range(11)]
Squares = [14, 4, 9, 9, 9, 9, 9, 9, 9, 9, 9]
print(sum(Squares))
if sum(Squares) < 100:
    Players.append('X')
    Squares.append(100-sum(Squares))
squares_per_player = {k: v for k, v in zip(Players, Squares)}

Sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(Players)

# The Vals, Rows and Cols sequences all follow this form
Vals = Players
Rows = Sequence
Cols = Sequence
 
# Define Problem       
prob = LpProblem("SuperBowl Problem",LpMinimize)

# Creating a Set of Variables
choices = LpVariable.dicts("Choice",(Vals,Rows,Cols),0,1,LpInteger)
# print(choices)

# Added arbitrary objective function
prob += 0, "Arbitrary Objective Function"

# A constraint ensuring that only one value can be in each square is created
for r in Rows:
    for c in Cols:
        prob += lpSum([choices[v][r][c] for v in Vals]) == 1, ""

# Add constraints that says there can only be minimum number of squares per player in each row or column
for v in Vals:
    for r in Rows:
        prob += lpSum([choices[v][r][c] for c in Cols]) <= (squares_per_player[v] // 10) + 1, ""
        
    for c in Cols:
        prob += lpSum([choices[v][r][c] for r in Rows]) <= (squares_per_player[v] // 10) + 1, ""

    print(v, squares_per_player[v])
    prob += lpSum([[choices[v][r][c] for r in Rows] for c in Cols]) == squares_per_player[v], ""
            

# Add constraints to minimize duplicates in rows and columns
prob += lpSum([[[choices[v][r][c] + choices[v][r][c2] for c in Cols for c2 in Cols if c != c2] for r in Rows] for v in Vals])  # Minimize duplicates in rows
prob += lpSum([[[choices[v][r][c] + choices[v][r2][c] for r in Rows for r2 in Rows if r != r2] for c in Cols] for v in Vals])  # Minimize duplicates in columns


# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# print out sudoku solution
print("\nSuper Bowl Squares Solution")
for r in Rows:
    for c in Cols:
        for v in Vals:
            if choices[v][r][c].varValue == 1:               
                print(v, end = " ")
    print("")
print("+-------+-------+-------+")