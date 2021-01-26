# from main import G as graph
from aco import ant_colony_optimization, get_path_length


def perform_tests(G):
    pheromone_level = 1.0
    pheromone_evap = 1.0
    result = {}
    to_test = [("Vancouver", "Boston"), ("Vancouver", "Miami"), ("Montreal", "Nashville")]
    # tested alpha and corresponding beta
    coeffs = {
        1: 2,
        -1: -0.5,
        2: 1,
        -0.5: 100,
        100: -0.5
        }
    iters_num = [1, 10, 40, 100]
    ants_num = [1, 10, 30]  # [1, 10, 30, '10rand']
    for vertices in to_test:
        source = vertices[0]
        destination = vertices[1]
        for alpha, beta in coeffs.items():
            for iters in iters_num:
                for ants in ants_num:
                    # if ants == '10rand':
                    #     ants = 10
                    solution = ant_colony_optimization(G, source, destination, ants, alpha, beta, pheromone_level, pheromone_evap, iters)
                    path_length = get_path_length(G, solution)
                    print(f"Path: {source} -> {destination}\nalpha: {alpha}, beta: {beta}\nmax_iters: {iters}\nants: {ants}\nsolution: {path_length}\n")
                    # result[(source, destination)][(alpha, beta)][iters_num][ants_num] = path_length
    # return result
