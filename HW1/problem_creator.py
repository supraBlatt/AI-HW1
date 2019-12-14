from ways import load_map_from_csv, tools
import random as rand
import . from route_finding_algorithms.py as algorithms
import . from cost_functions as funcs

def generate_problem_set(roads, size, dist_limit):
    problems = []

    # generate problems until we have 'size' problems
    with tools.dbopen('problems.csv', 'w') as f:
        while len(problems) < size:
            # generate a random source
            src = rand.randint(0, len(roads))
            visited = BFS(roads, src, dist_limit)
            dest = visited[rand.randint(0, len(visited))]
            p = (src, dest)

            # make the problems unique
            if p not in problems:
                problems.append(p)
                f.write(str(p[0]) + "," + str(p[1]) + '\n')

def BFS(roads, src, dist_limit):

    # Run a basic BFS code with a distance parameter
    visited = [False] * (len(roads))
    distance = 0
    queue = []

    # (junction index, distance from src)
    queue.append((src, 0))
    visited[src] = True

    while queue:
        s, dist = queue.pop(0)
        if dist >= dist_limit:
            continue

        # get all nearby junction indices
        SUCC = [link[1] for link in roads[s].links]
        for i in SUCC:
            if visited[i] == False:
                queue.append((i, dist + 1))
                visited[i] = True

    # return a list of the indices we visited
    return [i for i, val in enumerate(visited) if val]

def solve_problem(roads, alg_name):

    # make a dictionary between the algorithm name to its route finding function and heuristic function
    # because we'll need the heuristic function for questions 6, 9 and 11, for knowing what to print to the output file
    algs = {'UCS' : (algorithms.find_ucs_route, None),
            'AStar' : (algorithms.find_astar_route, funcs.heuristic_time),
            'IDAStar' : (algorithms.find_idastar_route, funcs.heuristic_time)}

    alg, heuristic = algs[alg_name]

    # open the problems we generated and solve them one by one, saving the time taken in a file
    with open('db/problems.csv', 'r') as problem_file, open('results/' + alg_name + "Runs.txt", 'w') as output_file:
        for line in problem_file:

            # for every problem: solve it, and output the actual time and estimated time
            src, target = line.split(",")
            path = alg[0](roads, src, target)
            path_time = str(funcs.path_time(roads, path))

            # if there a heuristic output also the estimated heuristic time
            if heuristic is not None:
                time_on_heuristic = heuristic(roads, src, target)
                output_file.write(str(time_on_heuristic) + "," + path_time + '\n')
            else:
                output_file.write(path_time + '\n')

if __name__ == '__main__':
    roads = load_map_from_csv()
    generate_problem_set(roads, 100, 25)