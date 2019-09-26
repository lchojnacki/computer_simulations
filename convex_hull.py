import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import time
from datetime import datetime
import line_profiler


class Point:
    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y


def turn_right(p1, p2, p3):
    cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    return cross < 0


def convex_hull(points):
    points.sort(key=lambda p: (p.x, p.y))
    number_of_points = len(points)
    l_top = points[:2]
    for i in range(2, number_of_points):
        l_top.append(points[i])
        while len(l_top) > 2 and \
        not turn_right(*l_top[-3:]):
            del l_top[-2]
    l_bottom = [points[-1], points[-2]]
    for i in range(number_of_points-3, -1, -1):
        l_bottom.append(points[i])
        while len(l_bottom) > 2 and \
        not turn_right(*l_bottom[-3:]):
            del l_bottom[-2]
    del l_bottom[0]
    del l_bottom[-1]
    l = l_top + l_bottom
    return l


def draw_convex_hull(points, hull_points):
    _, ax = plt.subplots()
    ax.grid(True)
    points_xy = [[], []]
    for p in points:
        points_xy[0].append(p.x)
        points_xy[1].append(p.y)
    ax.plot(points_xy[0], points_xy[1], '.')
    lines = []
    for i in range(len(hull_points)):
        lines.append((hull_points[i - 1], hull_points[i]))
    if lines is not None:
        for line in lines:
            new_line = Line2D([line[0].x, line[1].x], [line[0].y, line[1].y], color='red')
            ax.add_line(new_line)
    plt.show()


def test(number_of_points, draw=False):
    points = []
    for _ in range(number_of_points):
        points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    start = time.time()
    hull_points = convex_hull(points)
    end = time.time()

    if draw:
        draw_convex_hull(points, hull_points)


def profile_function(number_of_points):
    points = []
    for _ in range(number_of_points):
        points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    profile = line_profiler.LineProfiler(convex_hull)
    profile.runcall(convex_hull, points)
    now = datetime.now()
    file = open("python_profiler_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()


if __name__ == "__main__":
    num = int(input("Number of points: "))
    test(num, True)
