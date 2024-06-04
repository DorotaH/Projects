def is_polygon_convex(points):
    n = len(points)
    if n == 3:  # A triangle
        return True
    else:
        signs = []
        for i in range(n):
            dx1 = points[(i + 1) % n].x - points[i].x
            dy1 = points[(i + 1) % n].y - points[i].y
            dx2 = points[(i + 2) % n].x - points[(i + 1) % n].x
            dy2 = points[(i + 2) % n].y - points[(i + 1) % n].y

            z_cross_product = dx1 * dy2 - dy1 * dx2

            if z_cross_product != 0:
                signs.append(z_cross_product > 0)

        return all(signs) or not any(signs)
