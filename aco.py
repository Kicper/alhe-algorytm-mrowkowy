import math
import networkx as nx
import random
from typing import List
from ant import Ant


# m - ants number
# alpha - parameter that defines the influence of pheromones on the choice of next vertex
# beta - parameter that defines the influence of remaining data on the choice of next vertex
def ant_colony_optimization(graph: nx.Graph, source, destination, m, alpha, beta, starting_pheromone_level, evaporation_coeff, iters):
    # pheromone level and ants init
    graph, ants = init_environment(graph, m, starting_pheromone_level)
    print_pheromone(graph)
    current_best_solution = []
    current_best_distance = math.inf
    # or while convergence_met(): # todo
    for i in range(iters):
        ants, ants_in_destination = reset_ants(ants)
        # array of lost ants
        ants_lost = []
        # until every ant reach destination:
        while ants_in_destination + len(ants_lost) != m:
            # update_pheromones
            iter = 0
            
            for ant in ants:
                iter = iter + 1
                if not ant.has_reached_destination():
                    # visit new vertex
                    # if ant starting from source
                    if not ant.get_visited_vertices():
                        ant.set_visited(source)
                    current_vertex = ant.get_visited_vertices()[-1]
                    adjacent_data = get_allowed_vertices_data(graph, current_vertex, ant.get_visited_vertices())


                    if not adjacent_data:
                        if ant not in ants_lost:
                            ants_lost.append(ant)
                        continue
                    if(i >= 3):
                        next_vertex = pick_next_vertex(alpha, beta, current_vertex, adjacent_data)
                    else:
                        next_vertex = pick_next_vertex_random(alpha, beta, current_vertex, adjacent_data)
                    # print(f'ant {ants.index(ant)}\nnext vertex: {next_vertex}\n')
                    ant.set_visited(next_vertex)
                    if adjacent_data:
                        print_everything(graph, ant, iter, i)
                    # if ant has reached destination
                    if next_vertex == destination:
                        ant.reach_destination()
                        ants_in_destination += 1
                        solution = ant.get_visited_vertices()
                        solution_length = get_path_length(graph, solution)
                        current_best_solution, current_best_distance = set_best_solution(current_best_solution,
                                                                                            current_best_distance,
                                                                                            solution, solution_length)
                        # print(f'Ant {ants.index(ant)}, solution: {solution}, and best: {current_best_solution}\n')
            local_pheromone_update(graph, ants, starting_pheromone_level, evaporation_coeff, ants_lost)
        # global_pheromone_update(graph) # todo
    solution = current_best_solution
    print_pheromone(graph)
    return solution


def print_everything(g: nx.Graph, ant, iter, i):
    print("Which ant:", iter)
    print("Main loop:", i)
    print("Actual road:", ant.get_visited_vertices())
    print(ant.get_visited_vertices()[-2])
    print(ant.get_visited_vertices()[-1])
    print(g[ant.get_visited_vertices()[-2]][ant.get_visited_vertices()[-1]]['pheromone'])
    print("")


def print_pheromone(graph: nx.Graph):
    for e in graph.edges:
        print(graph.edges[e]['pheromone'])


def get_allowed_vertices_data(graph: nx.Graph, source, visited):
    # copy entries that are relevant
    allowed_neighbors = {}
    for adjacent in graph.adj[source]:
        if adjacent not in visited:
            allowed_neighbors[adjacent] = graph.adj[source][adjacent]
    return allowed_neighbors


def pick_next_vertex(alpha, beta, current, adj_data):
    highest_probability = 0.0
    next_vertex = current
    for vertex in adj_data:
        vertex_prob = get_vertex_probability(vertex, adj_data, alpha, beta)
        if vertex_prob > highest_probability:
            highest_probability = vertex_prob
            next_vertex = vertex
    return next_vertex


def pick_next_vertex_random(alpha, beta, current, adj_data):
    highest_probability = 0.0
    next_vertex = current

    rand = random.randint(0, 3)
    if(rand < 1):
        rand_vertex = random.randint(1, len(adj_data))
        i = 0
        for vertex in adj_data:
            i = i + 1
            if(i == rand_vertex):
                next_vertex = vertex
                return next_vertex
    else:
        for vertex in adj_data:
            vertex_prob = get_vertex_probability(vertex, adj_data, alpha, beta)
            if vertex_prob > highest_probability:
                highest_probability = vertex_prob
                next_vertex = vertex
        return next_vertex


def get_vertex_probability(destination, edges_data, alpha, beta):
    probability_numerator = edges_data[destination]['pheromone']**(alpha) * (1.0 / edges_data[destination]['cost'])**(beta)
    denominator_data = {}
    for end_vertex, edge in edges_data.items():
        denominator_data[end_vertex] = edge['pheromone'] **(alpha) * (1.0 / edge['cost'])**(beta)
    probability_denominator = sum(denominator_data.values())
    choice_probability = probability_numerator / probability_denominator
    return choice_probability


def get_path_length(graph: nx.Graph, path):
    distance = 0.0
    for vertex, next_vertex in zip(path, path[1:]):
        edge_length = graph.adj[vertex][next_vertex]['cost']
        distance += edge_length
    return distance


def set_best_solution(current_best, current_best_dist, to_check_solution, to_check_dist):
    if to_check_dist < current_best_dist:
        return to_check_solution, to_check_dist
    return current_best, current_best_dist


def init_environment(g: nx.Graph, ants_number, pheromone):
    for e in g.edges:
        g.edges[e]['pheromone'] = float(pheromone)
    ants = [Ant() for a in range(ants_number)]
    return g, ants


def reset_ants(ants: List[Ant]):
    for ant in ants:
        ant.reset_ant()
    ants_in_destination = 0
    return ants, ants_in_destination


def local_pheromone_update(graph: nx.Graph, ants: List[Ant], starting_pheromone, evaporation, ants_lost):
    for ant in ants:
        if(ant not in ants_lost):
            for i in range(len(ant.get_visited_vertices())-1):
                
                last_pheromone_level = graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['pheromone']
                amount_of_pheromone = 20/len(ant.get_visited_vertices())
                new_pheromone_level = (1.0 - evaporation)*last_pheromone_level + evaporation*amount_of_pheromone
                graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['pheromone'] = new_pheromone_level
    return


# def global_pheromone_update(graph: nx.Graph):
    # todo