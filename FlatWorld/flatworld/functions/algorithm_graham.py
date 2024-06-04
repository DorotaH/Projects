from .models import Stack, Point
import matplotlib.pyplot as plt
import matplotlib
import io
from random import randint
import matplotlib
matplotlib.use('TkAgg')


# O(n)
def generate(input_points):
    points = []
    for _ in range(input_points):
        x = randint(-200, 200)
        y = randint(-200, 200)
        points.append(Point(x, y))
    print(points)
    return points


# O(1)
def det(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2


# O(1)
def calculate_alfa(point, pivot):
    x, y = point.x - pivot.x, point.y - pivot.y
    d = abs(x) + abs(y)
    if d == 0:
        return 0
    if x >= 0 and y >= 0:
        return y / d
    elif x < 0 and y >= 0:
        return 2 - y / d
    elif x <= 0 and y < 0:
        return 2 + abs(y) / d
    elif x >= 0 and y < 0:
        return 4 - abs(y) / d
    else:
        return -1


def calculate_hull(input_points):
    points = generate(input_points)

    matplotlib.use("Agg")
    plt.figure()
    for i, point in enumerate(points, start=1):
        plt.plot(point.x, point.y, "bo")
        plt.text(point.x, point.y, str(i))

    points_to_return = points

    # Graham O(nlongn)
    min_y = float("inf")
    min_index = -1
    # szukamy punktu o najmniejszej współrzędnej y
    for i, point in enumerate(points):
        if point.y < min_y or (
            point.y == min_y and point.x < points[min_index].x
        ):
            min_y = point.y
            min_index = i
    # zamieniamy ten punkt z pierwszym
    points[0], points[min_index] = points[min_index], points[0]
    pivot = points[0]
    sorted_polar_points = sorted(
        points[1:], key=lambda p: calculate_alfa(p, pivot)
    )
    # wrzucamy pierwsze 3 punkty na stos
    Graham_stack = Stack()
    Graham_stack.push(points[0])
    Graham_stack.push(sorted_polar_points[0])
    Graham_stack.push(sorted_polar_points[1])

    # jeśli punkt p jest na prawo od poprzedniego wektora zamien ostatni element na stosie na p
    for i in range(1, len(sorted_polar_points)):
        while (
            len(Graham_stack.items) > 1
            and det(
                Graham_stack.items[-2],
                Graham_stack.items[-1],
                sorted_polar_points[i],
            )
            != 2  # jeśli det != 2 to znaczy, że punkt jest na prawo od wektora, czyli tworzy kąt wklęsły
        ):
            Graham_stack.pop()
        Graham_stack.push(sorted_polar_points[i])

    # struktura do przechowywania punktów
    hull_points = []
    while not Graham_stack.is_empty():
        point = Graham_stack.pop()
        hull_points.append(point)
    hull_points.append(hull_points[0])

    for i in range(len(hull_points) - 1):
        plt.plot(
            [hull_points[i].x, hull_points[i + 1].x],
            [hull_points[i].y, hull_points[i + 1].y],
            "c-",
        )
    for i, point in enumerate(hull_points, start=1):
        plt.plot(point.x, point.y, "go")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    image_data = buf.getvalue()
    world_points = [(point.x, point.y) for point in points_to_return]
    hull_points = [(point.x, point.y) for point in hull_points]
    return image_data, world_points, hull_points
