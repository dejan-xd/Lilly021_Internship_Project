import pygame as pg
import pygamebg
from string import ascii_uppercase
from termcolor import colored

WIDTH = HEIGHT = 500


def user_input():
    """
    Method for handling user inputs.
    :return:
    """
    list_vertices = []
    list_char = []

    # user input for number of vertices
    while True:
        try:
            num_vertices = int(input('Number of vertices: '))
            if num_vertices < 3:  # has to be more than 3 vertices to be a polygon
                print(colored("INFO >>> Number of vertices must be larger than 2.", "yellow"))
            elif num_vertices > 26:  # since Im using ascii_uppercase library there is no more than 26 letters
                print(colored("INFO >>> Number of vertices must be lesser than 26.", "yellow"))
            else:
                break
        except ValueError:
            print(colored("INFO >>> Number of vertices must be an integer!", "yellow"))

    # user input for creating vertices
    for i in range(num_vertices):
        while True:
            try:
                char = ascii_uppercase[i]  # assign letter for each vertex
                vertex = input('Vertex ' + str(i + 1) + ': ')
                vertex = list(map(int, vertex.split(' ')))  # convert strings to ints inside list coz we need tuple later on

                is_between_x = 1 <= vertex[0] <= WIDTH  # lock x to be inside canvas
                is_between_y = 1 <= vertex[1] <= WIDTH  # lock y to be inside canvas
                if is_between_x and is_between_y:
                    list_vertices.append(vertex)
                    list_char.append(char)
                else:
                    print(colored("INFO >>> X and Y must be between 1 and 499", "yellow"))
                    continue

            except ValueError:
                print(colored("INFO >>> Expected format: Integer Integer", "yellow"))
                continue
            else:
                break

    # user input for check vertex if it's inside the polygon
    while True:
        try:
            check_vertex = input('Check vertex: ')
            check_vertex = list(map(int, check_vertex.split(' ')))  # same as with vertex

            is_between_x = 1 <= check_vertex[0] <= 499  # lock x to be inside canvas
            is_between_y = 1 <= check_vertex[1] <= 499  # lock y to be inside canvas
            if not is_between_x and not is_between_y:
                print(colored("INFO >>> X and Y must be between 1 and 499", "yellow"))
                continue
        except ValueError:
            print(colored("INFO >>> Check vertex must be an integer!", "yellow"))
        else:
            break

    # call draw method and forward parameters
    draw(list_vertices, list_char, check_vertex)


def draw(list_vertices, list_char, check_vertex):
    """
    Draw method to display and show created polygon.
    :param list_vertices: list of vertices which store tuples
    :param list_char: list of names for each vertex
    :param check_vertex: check vertex tuple to determine if it's inside polygon
    :return:
    """
    bg_color = pg.Color("gray")
    line_color = pg.Color("blue")
    point_color = pg.Color("black")
    canvas = pygamebg.open_window(WIDTH, HEIGHT, "Project")
    canvas_running = True
    font = pg.font.SysFont("Arial", 15)
    text = font.render(ascii_uppercase[len(list_char)], True, point_color)  # notation for check_vertex point
    flag = True  # flag to display check methods only once

    # canvas loop
    while canvas_running:
        for event in pg.event.get():  # loop through all active events
            if event.type == pg.QUIT:  # Close the program if the user presses the 'X'
                canvas_running = False

        canvas.fill(bg_color)  # fill canvas
        pg.draw.polygon(canvas, line_color, list_vertices, 1)  # draw polygon with vertices from list_vertices

        # writing vertex names on canvas
        index = 0
        for txt in list_char:
            char = font.render(txt, True, point_color)
            canvas.blit(char, list_vertices[index])  # draw polygon point name on canvas
            pg.draw.circle(canvas, point_color, list_vertices[index], 4)  # draw vertex points as small circles
            index += 1

        canvas.blit(text, check_vertex)  # draw polygon point name on canvas
        pg.draw.circle(canvas, point_color, check_vertex, 4)  # draw check_vertex on canvas

        # check if check_point is inside polygon and if polygon is convex
        if flag:  # print only once
            if is_point_inside_polygon(check_vertex[0], check_vertex[1], list_vertices):
                print(colored("Point inside polygon? >>> TRUE", "green"))
            else:
                print(colored("Point inside polygon? >>> FALSE", "red"))
            if is_convex(list_vertices):
                print(colored("Is polygon convex? >>> TRUE", "green"))
            else:
                print(colored("Is polygon convex? >>> FALSE", "red"))
            flag = False

        # update display
        pg.display.update()


def is_point_inside_polygon(x, y, polygon):
    """
    Determine if a point is inside a given polygon or not. Polygon is a list of (x,y) pairs.
    :param x: x value of check_vertex
    :param y: y value of check_vertex
    :param polygon: list of tuples which form polygon
    :return:
    """
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]  # last vertex is first vertex
        if y > min(p1y, p2y):  # if check_vertex y is between min and max of two connected vertices
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):  # if check_vertex x is less than max of two connected vertices
                    if p1y != p2y:
                        x_intersects = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x  # format line for intersection
                        if p1x == p2x or x <= x_intersects:
                            inside = not inside  # if odd times return True if even return False
        p1x, p1y = p2x, p2y  # point 2 is now point 1
    return inside


def is_convex(list_vertices):
    """
    Check if polygon is convex or not.
    :param list_vertices:  list of vertices
    :return:
    """
    cross_product_list = []
    for i in range(len(list_vertices)):
        p1 = list_vertices[i]
        if i - 1 < 0:  # if index is first in list
            p0 = list_vertices[len(list_vertices) - 1]  # take last element from list
        else:
            p0 = list_vertices[i - 1]
        if i + 1 > len(list_vertices) - 1:  # if index is last in list
            p2 = list_vertices[0]  # take first element from list
        else:
            p2 = list_vertices[i + 1]

        dx1 = p1[0] - p0[0]  # current index x - left index x
        dy1 = p1[1] - p0[1]  # current index y - left index y
        dx2 = p2[0] - p1[0]  # right index x - current index x
        dy2 = p2[1] - p1[1]  # right index y - current index y
        z_cross_product = dx1 * dy2 - dy1 * dx2  # cross product of the vectors
        cross_product_list.append(z_cross_product)

    if all(i >= 0 for i in cross_product_list):  # if all values in cross_product_list are positive including zero
        return True
    elif all(i < 0 for i in cross_product_list):  # if all values in cross_product_list are negative
        return True
    else:
        return False


# run method
user_input()
