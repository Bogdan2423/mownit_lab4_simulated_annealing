import random
import math
import matplotlib.pyplot as plt

T = 50
T_change = 0.8
changes = 3
counter = 0

points = [(2, 1), (3, 7), (4, 2), (15, 13), (11, 10), (12, 14), (1, 14), (3, 11), (2, 18)]
dist = 0
dist_list = []
for i in range(1, len(points)):
    dist += math.dist(points[i - 1], points[i])
dist += math.dist(points[0], points[len(points) - 1])

dist_list.append(dist)
while counter < 20:
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
            prob = math.exp((dist-new_dist) / T)
            if random.uniform(0, 1) > prob:  # swap back
                points[per1], points[per2] = points[per2], points[per1]
                swapped = False

        if swapped:
            dist = new_dist

        dist_list.append(dist)

    counter += 1
    T *= T_change

plt.plot(dist_list)
plt.show()