from heapq import heappush, heappop
from . import cost_functions as funcs

def find_ucs_route(roads, source, target, cost_func=funcs.compute_time):
    frontier = []

    # (path_cost, path)
    heappush(frontier, (0, [source]))
    explored = [False] * len(roads)

    while frontier:
        cost, path = heappop(frontier)

        # the last node in our path
        cur = path[-1]
        if cur == target:
            return path

        explored[cur] = True

        # go over neighboring junctions and push new paths to queue
        for link in roads[cur].links:
            child = link.target
            if not explored[child]:

                # push the new path to the frontier (the priority queue heap)
                heappush(frontier, (cost + cost_func(link), path + [child]))

    # mission failed
    return []

def find_astar_route(roads, source, target, cost_func=funcs.compute_time, heuristic_func=funcs.heuristic_time):

    'call function to find path, and return list of indices'
    frontier = []

    # (path_f, path_g, path)
    heappush(frontier, (0, 0, [source]))
    explored = []

    while frontier:

        # get the current best path
        cost_f, cost_g, path = heappop(frontier)
        cur = path[-1]
        explored[cur] = True

        # found the goal
        if cur == target:
            return path

        for link in roads[cur].links:
            child = link.target
            if not explored[child]:
                child_g = cost_g + cost_func(link)
                child_h = heuristic_func(roads, child, target)
                child_f = child_g + child_h

                #check if it's in the open list and if we beat the G score
                in_open_list = [item for item in frontier if item[2] is path]
                if len(in_open_list):
                    node = in_open_list[0]
                    if node[1] < child_g:
                        continue

                heappush(frontier, (child_f, child_g, path + [child]))

    # mission failed
    return []

def find_idastar_route(roads, source, target, cost_func = funcs.compute_time, heuristic_func = funcs.heuristic_time):
    'call function to find path, and return list of indices'
    raise NotImplementedError
