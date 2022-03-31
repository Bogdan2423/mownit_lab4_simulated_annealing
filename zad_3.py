import random
import math
import matplotlib.pyplot as plt

T = 5000
T_change = 0.99
changes = 50000
counter = 0

sudoku = [[-1 for _ in range(9)] for _ in range(9)]
fixed = [[False for _ in range(9)] for _ in range(9)]

def add_fixed(sudoku, row, col, val):
    sudoku[row][col] = val
    fixed[row][col] = True

add_fixed(sudoku, 0, 7, 1)
add_fixed(sudoku, 1, 5, 2)
add_fixed(sudoku, 1, 8, 3)
add_fixed(sudoku, 2, 3, 4)
add_fixed(sudoku, 3, 6, 5)
add_fixed(sudoku, 4, 0, 6)
add_fixed(sudoku, 4, 2, 1)
add_fixed(sudoku, 4, 3, 7)
add_fixed(sudoku, 5, 2, 4)
add_fixed(sudoku, 5, 3, 1)
add_fixed(sudoku, 6, 1, 5)
add_fixed(sudoku, 6, 6, 2)
add_fixed(sudoku, 7, 4, 8)
add_fixed(sudoku, 7, 7, 6)
add_fixed(sudoku, 8, 1, 3)
add_fixed(sudoku, 8, 3, 9)
add_fixed(sudoku, 8, 4, 1)

squares = [(0, 0), (3, 0), (6,0),
           (0, 3), (3, 3), (6, 3),
           (0, 6), (3, 6), (6, 6)]

inside_square = [(0, 0), (0, 1), (0, 2),
                 (1, 0), (1, 1), (1, 2),
                 (2, 0), (2, 1), (2, 2)]

duplicates_in_row = [0 for _ in range(9)]
duplicates_in_col = [0 for _ in range(9)]

for x,y in squares:
    numbers_to_fill=[i for i in range(1,10)]
    for i in range(3):
        for j in range(3):
            if fixed[x+i][y+j]:
                numbers_to_fill.remove(sudoku[x+i][y+j])
    random.shuffle(numbers_to_fill)
    k=0
    for i in range(3):
        for j in range(3):
            if not fixed[x+i][y+j]:
                sudoku[x+i][y+j]=numbers_to_fill[k]
                k+=1

for row in sudoku:
    print(row)

def calc_val(sudoku, duplicates_in_row, duplicates_in_col, row, col):
    already_in_row = [False for _ in range(9)]
    already_in_col = [False for _ in range(9)]
    duplicates_in_col[col]=0
    duplicates_in_row[row]=0
    for i in range(9):
        if already_in_row[sudoku[row][i]-1]:
            duplicates_in_row[row] += 1
        else:
            already_in_row[sudoku[row][i]-1] = True

        if already_in_col[sudoku[i][col]-1]:
            duplicates_in_col[col] += 1
        else:
            already_in_col[sudoku[i][col]-1] = True

for i in range(9):
    calc_val(sudoku, duplicates_in_row, duplicates_in_col, i, i)

val = sum(duplicates_in_row)+sum(duplicates_in_col)

val_list=[]

while val>0:
    for i in range(changes):
        swapped=False
        x, y = squares[random.randint(0, 8)]
        a = random.randint(0,8)
        a_x = x+inside_square[a][0]
        a_y = y+inside_square[a][1]
        while fixed[a_x][a_y]:
            a = random.randint(0, 8)
            a_x = x + inside_square[a][0]
            a_y = y + inside_square[a][1]
        b = random.randint(0, 8)
        while b == a:
            b = random.randint(0, 8)
        b_x = x + inside_square[b][0]
        b_y = y + inside_square[b][1]
        while fixed[b_x][b_y]:
            b = random.randint(0, 8)
            while b == a:
                b = random.randint(0, 8)
            b_x = x + inside_square[b][0]
            b_y = y + inside_square[b][1]

        sudoku[a_x][a_y], sudoku[b_x][b_y] = sudoku[b_x][b_y], sudoku[a_x][a_y]
        calc_val(sudoku, duplicates_in_row, duplicates_in_col, a_x, a_y)
        calc_val(sudoku, duplicates_in_row, duplicates_in_col, b_x, b_y)
        new_val = sum(duplicates_in_row) + sum(duplicates_in_col)
        swapped = True
        if new_val == 0:
            break

        if new_val > val:
            prob = math.exp((val - new_val) / T)
            if random.uniform(0, 1) > prob:  # swap back
                sudoku[a_x][a_y], sudoku[b_x][b_y] = sudoku[b_x][b_y], sudoku[a_x][a_y]
                calc_val(sudoku, duplicates_in_row, duplicates_in_col, a_x, a_y)
                calc_val(sudoku, duplicates_in_row, duplicates_in_col, b_x, b_y)
                swapped = False

        if swapped:
            val = new_val

        val_list.append(val)
        counter += 1
        print(counter, val)
    T *= T_change

for row in sudoku:
    print(row)

plt.plot(val_list)
plt.show()