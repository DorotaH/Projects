from collections import deque
from random import randint


class Stack:
    def __init__(self):
        self.items = deque()

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False


class inhabitants:
    def __init__(self, id):
        self.id = id
        self.personality = randint(0, 1)
        self.direction = randint(0, 1)

    def __str__(self):
        return f"({self.id}, {self.personality}, {self.direction})"

    __repr__ = __str__

    def to_dict(self):
        return {
            "id": self.id,
            "personality": self.personality,
            "direction": self.direction,
        }


class Guard:
    def __init__(self, id, energy, max_steps):
        self.id = id
        self.energy = energy
        self.patrol_day = 0
        self.max_steps = max_steps

    def set_patrol_day(self, day):
        self.patrol_day = day
        
class Node:
    def __init__(self,name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
    
    def __hash__(self):
        return hash(self.name)

class Edge:
    def __init__(self,froom,to,cost,flow):
        self.froom = froom
        self.to = to
        self.cost = cost
        self.flow = flow

    def __str__(self):
        return f'{self.froom.name} {self.to.name} {self.cost} {self.flow}'
    
    def delete_edge(self):
        self.cost = 99999 
    
class Graf:
    def __init__(self):
        self.Nodes = []
        self.Edges = []
        self.max_value = 0


    def add_node(self,Node):
        self.Nodes.append(Node)


    def add_edge(self,Edge):
        self.Edges.append(Edge)
        self.max_value += Edge.flow
