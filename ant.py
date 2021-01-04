class Ant:
    def __init__(self):
        self.visited_vertices = []
        self.reached_destination = False

    def set_visited(self, vertex):
        self.visited_vertices.append(vertex)

    def reset_visited(self):
        self.visited_vertices = []

    def get_visited_vertices(self):
        return self.visited_vertices

    def has_reached_destination(self):
        return self.reached_destination

    def reset_ant(self):
        self.reset_visited()
        self.reached_destination = False

    def reach_destination(self):
        self.reached_destination = True
