import networkx as nx
import math
from aco import ant_colony_optimization


G = nx.Graph()


def read_file():
    with open( 'input.txt', 'r' ) as file:
        line = file.readline()
        while( "NODES" not in line ):
            line = file.readline()
        line = file.readline()
        splitted = line.split()
        while( ")" not in splitted[0] ):
            G.add_node(splitted[0], longitude=float(splitted[2]), latitude=float(splitted[3]), real_cost=float('inf'), tentative_cost=float('inf'), prev_node="")
            line = file.readline()
            splitted = line.split()
        while( "LINKS" not in line ):
            line = file.readline()
        line = file.readline()
        splitted = line.split()
        while( ")" not in splitted[0] ):
            G.add_edge(splitted[2], splitted[3], cost=float(splitted[11]))
            line = file.readline()
            splitted = line.split()


def ant_algorithm():
    
    ants_number = 10
    alpha = 1.0
    beta = 1.0
    pheromone_level = 1.0
    max_iters = 10
    pheromone_evaporation = 0.1
    source_coords, destination_coords = "Vancouver", "Houston"

    solution = ant_colony_optimization(G, source_coords, destination_coords, ants_number, alpha, beta, pheromone_level, pheromone_evaporation, max_iters)
    # this one is quickest path which one ant has travelled
    print("Best solution based on best ant:")
    print(solution)


def main():
    read_file()
    ant_algorithm()


main()