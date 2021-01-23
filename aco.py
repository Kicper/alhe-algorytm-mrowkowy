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
        iter = 0
        for ant in ants:
            # while ants_in_destination + len(ants_lost) != m:
            # update_pheromones
            iter = iter + 1
            #print(iter)
            while not ant.has_reached_destination():
                # visit new vertex
                # if ant starting from source
                if not ant.get_visited_vertices():
                    ant.set_visited(source)
                current_vertex = ant.get_visited_vertices()[-1]
                adjacent_data = get_allowed_vertices_data(graph, current_vertex, ant.get_visited_vertices())

                if not adjacent_data:
                    if ant not in ants_lost:
                        ants_lost.append(ant)
                    #print(" ANT IS LOST! ", end="\t")
                    #print(ants_lost)
                    break
                next_vertex = pick_next_vertex(alpha, beta, current_vertex, adjacent_data, i, iters)
                # print(f'ant {ants.index(ant)}\nnext vertex: {next_vertex}\n')
                ant.set_visited(next_vertex)
                #if adjacent_data:
                #    print_everything(graph, ant, iter, i)
                # if ant has reached destination
                if next_vertex == destination:
                    #print(" DESTINATION! ")
                    ant.reach_destination()
                    ants_in_destination += 1
                    solution = ant.get_visited_vertices()
                    solution_length = get_path_length(graph, solution)
                    current_best_solution, current_best_distance = set_best_solution(current_best_solution,
                                                                                        current_best_distance,
                                                                                        solution, solution_length)
                        # print(f'Ant {ants.index(ant)}, solution: {solution}, and best: {current_best_solution}\n')
        global_pheromone_update(graph, ants, starting_pheromone_level, evaporation_coeff, ants_lost)
    solution = current_best_solution
    print_pheromone(graph)
    # solution based on pheromone path
    #result = solution_pheromone(source, destination, graph)
    return solution


def print_everything(g: nx.Graph, ant, iter, i):
    print("Which ant:", iter)
    print("Main loop:", i)
    print("Actual road:", ant.get_visited_vertices())
    print(ant.get_visited_vertices()[-2])
    print(ant.get_visited_vertices()[-1])
    print(g[ant.get_visited_vertices()[-2]][ant.get_visited_vertices()[-1]]['pheromone'])
    print()


def print_pheromone(graph: nx.Graph):
    for i in graph.nodes:
        for j in graph.nodes:
            if graph.has_edge(i, j):
                print(i, end="\t")
                print(j, end="\t")
                print(graph[i][j]['pheromone'])


def get_allowed_vertices_data(graph: nx.Graph, source, visited):
    # copy entries that are relevant
    allowed_neighbors = {}
    for adjacent in graph.adj[source]:
        if adjacent not in visited:
            allowed_neighbors[adjacent] = graph.adj[source][adjacent]
    return allowed_neighbors


def pick_next_vertex(alpha, beta, current, adj_data, iter, iters):
    highest_probability = 0.0
    next_vertex = current

    # first 20% of iterations is rand on 50%
    if(iter < iters/5):
        rand = random.randint(0, 10)
        if(rand < 5):
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
    # then 13,3% of iterations is rand on 30%
    elif(iter < iters/3):
        rand = random.randint(0, 10)
        if(rand < 3):
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
        denominator_data[end_vertex] = edge['pheromone']**(alpha) * (1.0 / edge['cost'])**(beta)
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


def global_pheromone_update(graph: nx.Graph, ants, starting_pheromone, evaporation, ants_lost):
    for ant in ants:
        if(ant not in ants_lost):
            # this part is used just for getting amount of distance:
            # from here
            sum_distance = 0
            for i in range(len(ant.get_visited_vertices())-1):
                print(graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['cost'])
                sum_distance = sum_distance + graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['cost']
            # to here
            for i in range(len(ant.get_visited_vertices())-1):
                
                last_pheromone_level = graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['pheromone']
                # case when shotrest path is that one which has the least amount of nodes:
                # from here
                # amount_of_pheromone = 1000/len(ant.get_visited_vertices())
                # to here
                # case when shotrest path is that one which has the least amount of distance:
                # from here
                amount_of_pheromone = 1000/sum_distance * graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['cost']
                # to here
                new_pheromone_level = (1.0 - evaporation)*last_pheromone_level + evaporation*amount_of_pheromone
                graph[ant.get_visited_vertices()[i]][ant.get_visited_vertices()[i+1]]['pheromone'] = new_pheromone_level
    return


def solution_pheromone(source, destination, graph):
    temp = source
    path = []
    path.append(source)
    while(graph.nodes[temp] != "destination"):
        print(path)
        for adjacent in graph.adj[temp]:
            max = 0
            next_node = 0
            if adjacent not in path:
                if max < graph[temp][adjacent]['cost']:
                    max = graph[temp][adjacent]['cost']
                    next_node = adjacent
        if max == 0:
            return "error"
        else:
            path.append(next_node)
    print("The shortest path to destination:")
    print(path)
    return path