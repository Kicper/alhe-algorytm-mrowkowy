import networkx as nx
import math

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


def get_user_input():
    print("Enter starting node:")
    start_node = input() 
    print("Enter destination node:")
    destination_node = input()
    return start_node, destination_node


def get_path(start, end):
    temp = end
    path = []
    while( G.nodes[temp]['prev_node'] != ""):
        path.insert(0, temp)
        temp = G.nodes[temp]['prev_node']
    path.insert(0, temp)
    path.insert(0, start)
    print("The shortest path to destination:")
    print(path)


def heuristic(start, end):
    x1 = G.nodes[start]['longitude']
    y1 = G.nodes[start]['latitude']
    x2 = G.nodes[end]['longitude']
    y2 = G.nodes[end]['latitude']
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )


def A_star(start, end):
    G.nodes[start]['real_cost'] = 0
    G.nodes[start]['tentative_cost'] = G.nodes[start]['real_cost'] + heuristic(start, end)
    if(start == end):
        print("Starting node is destination one!")
        return

    to_visit = list(G.neighbors(start))
    visited = []
    visited.append(start)
    curr_node = start

    for i in G.neighbors(curr_node):
        G.nodes[i]['real_cost'] = G.nodes[curr_node]['real_cost'] + G[curr_node][i]['cost']
        G.nodes[i]['tentative_cost'] = G.nodes[i]['real_cost'] + heuristic(i, end)

    while(to_visit != []):
        min = float('inf')
        node_min = float('inf')
        for i in to_visit:
            if( G.nodes[i]['tentative_cost'] < min ):
                min = G.nodes[i]['tentative_cost']
                node_min = i
        curr_node = node_min
        to_visit.remove(curr_node)
        visited.append(curr_node)
        if(curr_node == end):
            get_path(start, end)
            break

        for i in G.neighbors(curr_node):
            if(i not in visited and i not in to_visit):
                to_visit.append(i)
            if(i not in visited):
                real_cost = G.nodes[curr_node]['real_cost'] + G[curr_node][i]['cost']
                tentative_cost = real_cost + heuristic(i, end)
                if( tentative_cost < G.nodes[i]['tentative_cost'] ):
                    G.nodes[i]['tentative_cost'] = tentative_cost
                    G.nodes[i]['real_cost'] = real_cost
                    G.nodes[i]['prev_node'] = curr_node
                    

def main():
    read_file()
    start, end = "Vancouver", "Houston" #get_user_input()
    A_star(start, end)


main()