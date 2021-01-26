import networkx as nx
from aco import ant_colony_optimization
from algorithm_A import A_star
import sys
from tests import perform_tests

G = nx.Graph()


def read_file(filename: str):
    with open( filename, 'r' ) as file:
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


def ant_algorithm(source, destination):
    
    ants_number = 10
    alpha = 1.0
    beta = 1.0
    pheromone_level = 1.0
    max_iters = 10
    pheromone_evaporation = 0.1
    source_coords, destination_coords = source, destination

    solution = ant_colony_optimization(G, source_coords, destination_coords, ants_number, alpha, beta, pheromone_level, pheromone_evaporation, max_iters)
    # this one is quickest path which one ant has travelled
    print("Best solution based on best ant:")
    print(solution)


if __name__ == "__main__":
    args_num = len(sys.argv)
    if args_num > 1:
        read_file(sys.argv[1])
        if args_num == 2:
            perform_tests(G)
        elif args_num == 3 or args_num > 4:
            print("WRONG ARGUMENTS NUMBER\nEXIT", file=sys.stderr)
        else:
            source, destination = sys.argv[2], sys.argv[3]
            if source not in G.nodes or destination not in G.nodes:
                print("WRONG ARGUMENT NO GIVEN NODE IN GRAPH\nEXIT", file=sys.stderr)
                sys.exit(1)
            print('Ant colony results:')
            ant_algorithm(source, destination)

            print('\nA star solution:')
            A_star(G, source, destination)

            print('\nDijkstra algorithm solution:')
            print(nx.shortest_path(G, source=source, target=destination, weight='cost', method='dijkstra'))

            print('\nBellman-Ford algorithm solution:')
            print(nx.shortest_path(G, source=source, target=destination, weight='cost', method='bellman-ford'))
    else:
        print("NO INPUT FILE\nEXIT", file=sys.stderr)
