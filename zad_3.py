import random
import math
import matplotlib.pyplot as plt

T = 5
T_change = 0.99
changes = 500
counter = 0

sudoku = [[-1 for _ in range(9)] for _ in range(9)]
fixed = [[False for _ in range(9)] for _ in range(9)]

f = open("sudoku.txt")
for i in range(9):
    line = f.readline()
    for j in range(9):
        if line[j] != 'x':
            sudoku[i][j] = int(line[j])
            fixed[i][j] = True

squares = [(0, 0), (3, 0), (6, 0),
           (0, 3), (3, 3), (6, 3),
           (0, 6), (3, 6), (6, 6)]

inside_square = [(0, 0), (0, 1), (0, 2),
                 (1, 0), (1, 1), (1, 2),
                 (2, 0), (2, 1), (2, 2)]

duplicates_in_row = [0 for _ in range(9)]
duplicates_in_col = [0 for _ in range(9)]

for x, y in squares:
    numbers_to_fill = [i for i in range(1, 10)]
    for i in range(3):
        for j in range(3):
            if fixed[x + i][y + j]:
                numbers_to_fill.remove(sudoku[x + i][y + j])
    random.shuffle(numbers_to_fill)
    k = 0
    for i in range(3):
        for j in range(3):
            if not fixed[x + i][y + j]:
                sudoku[x + i][y + j] = numbers_to_fill[k]
                k += 1

for row in sudoku:
    print(row)
print("\n\n")


def calc_val(sudoku, duplicates_in_row, duplicates_in_col, row, col):
    already_in_row = [False for _ in range(9)]
    already_in_col = [False for _ in range(9)]
    duplicates_in_col[col] = 0
    duplicates_in_row[row] = 0
    for i in range(9):
        if already_in_row[sudoku[row][i] - 1]:
            duplicates_in_row[row] += 1
        else:
            already_in_row[sudoku[row][i] - 1] = True

        if already_in_col[sudoku[i][col] - 1]:
            duplicates_in_col[col] += 1
        else:
            already_in_col[sudoku[i][col] - 1] = True


for i in range(9):
    calc_val(sudoku, duplicates_in_row, duplicates_in_col, i, i)

val = sum(duplicates_in_row) + sum(duplicates_in_col)

val_list = []


def fixed_inside_square(square, fixed):
    counter = 0
    for i in range(3):
        for j in range(3):
            if fixed[square[0] + i][square[1] + j]:
                counter += 1
    return counter


while val > 0 and counter < 10000000:
    for i in range(changes):
        print(counter, val)
        swapped = False
        x, y = squares[random.randint(0, 8)]
        while fixed_inside_square((x, y), fixed) >= 8:
            x, y = squares[random.randint(0, 8)]
        a = random.randint(0, 8)
        a_x = x + inside_square[a][0]
        a_y = y + inside_square[a][1]
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
            val = new_val
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
    T *= T_change

for row in sudoku:
    print(row)

plt.plot(val_list)
plt.show()
