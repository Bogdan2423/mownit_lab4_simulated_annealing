import random
import math
import matplotlib.pyplot as plt
import random

T = 50
T_change = 0.99
changes = 10
counter = 0


def generate_points(n):
    points = []
    for i in range(n):
        points.append((random.randint(1, 2 * n), random.randint(1, 2 * n)))
    return points


# points = [(2, 1), (15, 13), (3, 7),(3, 11), (4, 2), (11, 10), (12, 14), (1, 14),  (2, 18)]
points = generate_points(50)


def draw_points(points, dist):
    plt.scatter(points[0][0], points[0][1])
    for i in range(1, len(points)):
        plt.scatter(points[i][0], points[i][1])
        plt.plot([points[i - 1][0], points[i][0]], [points[i - 1][1], points[i][1]])
    plt.plot([points[0][0], points[len(points) - 1][0]], [points[0][1], points[len(points) - 1][1]])
    plt.title("Total distance: " + str(round(dist, 2)))
    plt.show()


dist = 0
dist_list = []
for i in range(1, len(points)):
    dist += math.dist(points[i - 1], points[i])
dist += math.dist(points[0], points[len(points) - 1])

draw_points(points, dist)

dist_list.append(dist)
while counter < 1000:
    for i in range(changes):
        per1 = random.randrange(len(points))
        per2 = random.randrange(len(points))
        swapped = False
        while per2 == per1:
            per2 = random.randrange(len(points))
        if per1 > per2:
            per1, per2 = per2, per1

        new_dist = dist
        if per1 == 0:
            new_dist -= math.dist(points[len(points) - 1], points[per1])
        else:
            new_dist -= math.dist(points[per1 - 1], points[per1])
        new_dist -= math.dist(points[per1 + 1], points[per1])
        new_dist -= math.dist(points[per2 - 1], points[per2])
        if per2 == len(points) - 1:
            new_dist -= math.dist(points[0], points[per2])
        else:
            new_dist -= math.dist(points[per2 + 1], points[per2])

        points[per1], points[per2] = points[per2], points[per1]
        swapped = True

        if per1 == 0:
            new_dist += math.dist(points[len(points) - 1], points[per1])
        else:
            new_dist += math.dist(points[per1 - 1], points[per1])
        new_dist += math.dist(points[per1 + 1], points[per1])
        new_dist += math.dist(points[per2 - 1], points[per2])
        if per2 == len(points) - 1:
            new_dist += math.dist(points[0], points[per2])
        else:
            new_dist += math.dist(points[per2 + 1], points[per2])

        if new_dist > dist:
            prob = math.exp((dist - new_dist) / T)
            if random.uniform(0, 1) > prob:  # swap back
                points[per1], points[per2] = points[per2], points[per1]
                swapped = False

        if swapped:
            dist = new_dist

        dist_list.append(dist)

    counter += 1
    T *= T_change

draw_points(points, dist)

plt.title("Distance plot")
plt.plot(dist_list)
plt.show()
