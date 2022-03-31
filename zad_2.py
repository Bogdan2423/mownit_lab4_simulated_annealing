import random
import math
import matplotlib.pyplot as plt

T = 500
T_change = 0.99
changes = 500
counter = 0
N = 256

grid = [[0 for _ in range(N)] for _ in range(N)]
point_list = []
def add_to_grid(grid,point_list,x,y):
    grid[x][y]=1
    point_list.append((x,y))

def generate_randomly(grid,point_list,density):
    N=len(grid)
    points_num=int(N*N*density)
    for i in range(points_num):
        new_point=(random.randint(0,N-1),random.randint(0,N-1))
        while new_point in point_list:
            new_point = (random.randint(0, N - 1), random.randint(0, N - 1))
        add_to_grid(grid,point_list,new_point[0],new_point[1])

generate_randomly(grid,point_list,0.2)


neighborhood=[(-1,1),(0,1),(1,1),
              (-1,0),(0,0),(1,0),
              (-1,-1),(0,-1),(1,-1)]

reverse_neighborhood=neighborhood

move=[(-1,1),(0,1),(1,1),
      (-1,0),(0,0),(1,0),
      (-1,-1),(0,-1),(1,-1)]

def get_coordinate(x,move,N):
    if x+move<0:
        return N+x+move
    if x+move>N-1:
        return (x+move)-N
    return x+move

def get_energy(grid,neighborhood,x,y,N):
    energy=0
    if grid[x][y]:
        for x_offset, y_offset in neighborhood:
            if grid[get_coordinate(x,x_offset,N)][get_coordinate(y,y_offset,N)]:
                energy+=1
    return energy

total_energy=0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        total_energy+=get_energy(grid,neighborhood,i,j,N)

energy_list=[total_energy]

while counter < 2000:
    for i in range(changes):
        a_x, a_y=random.choice(point_list)
        x_move,y_move=random.choice(move)
        moved_x=get_coordinate(a_x,x_move,N)
        moved_y=get_coordinate(a_y,y_move,N)
        while grid[moved_x][moved_y]:
            a_x, a_y = random.choice(point_list)
            x_move, y_move = random.choice(move)
            moved_x = get_coordinate(a_x, x_move, N)
            moved_y = get_coordinate(a_y, y_move, N)
        to_recalculate=set()
        to_recalculate.add((a_x,a_y))
        to_recalculate.add((moved_x, moved_y))
        for neigh_x,neigh_y in neighborhood:
            to_recalculate.add((get_coordinate(a_x,neigh_x,N),get_coordinate(a_y,neigh_y,N)))
            to_recalculate.add((get_coordinate(moved_x,neigh_x,N), get_coordinate(moved_y,neigh_y,N)))

        new_energy=total_energy
        for calc_x,calc_y in to_recalculate:
            new_energy-=get_energy(grid,neighborhood,calc_x,calc_y,N)

        grid[a_x][a_y]=0
        point_list.remove((a_x,a_y))
        grid[moved_x][moved_y]=1
        point_list.append((moved_x, moved_y))
        swapped=True

        for calc_x,calc_y in to_recalculate:
            new_energy+=get_energy(grid,neighborhood,calc_x,calc_y,N)

        if new_energy>total_energy:
            prob = math.exp((total_energy - new_energy) / T)
            if random.uniform(0, 1) > prob:  # swap back
                grid[a_x][a_y] = 1
                point_list.append((a_x, a_y))
                grid[moved_x][moved_y] = 0
                point_list.remove((moved_x, moved_y))
                swapped = False

        if swapped:
            total_energy=new_energy
        energy_list.append(total_energy)
        print(total_energy)

    T*=T_change
    counter+=1

plt.plot(energy_list)
plt.show()