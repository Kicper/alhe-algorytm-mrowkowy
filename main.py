import networkx as nx
import math
from aco import ant_colony_optimization

# testing graph
G = nx.Graph()
G.add_nodes_from([(3, 8), (10, 7), (10, 3), (8, 1), (4, 3), (7, 6)])
G.add_edges_from([((3, 8), (10, 7)), ((3, 8), (7, 6)), ((3, 8), (4, 3)),
                  ((10, 7), (7, 6)), ((10, 7), (10, 3)),
                  ((10, 3), (4, 3)), ((10, 3), (8, 1)),
                  ((8, 1), (4, 3)),
                  ((4, 3), (7, 6))])
for e in G.edges:
    # euclidean distance
    weight = math.sqrt((e[0][0] - e[1][0])**2 + (e[0][1] - e[1][1])**2)
    G.edges[e]['weight'] = weight
source_coords = (7, 6)
destination_coords = (8, 1)

ants_number = 3
alpha = 1.0
beta = 1.0
pheromone_level = 1.0
max_iters = 10
pheromone_evaporation = 0.1

solution = ant_colony_optimization(G, source_coords, destination_coords, ants_number, alpha, beta, pheromone_level, pheromone_evaporation, max_iters)
print(solution)

