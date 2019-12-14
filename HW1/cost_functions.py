from ways import compute_distance, info

speeds = info.SPEED_RANGES
maxspeeds = [speed_range[1] for speed_range in speeds]

# compute the minimal time it would take to traverse a given link
def compute_time(link):

    # compute shortest traversal time = distance / maximum speed
    distance = link.distance
    max_speed =  maxspeeds[link.highway_type]
    return distance / max_speed

# overall time it would take to traverse a path
def path_time(roads, path):

    overall_time = 0
    for cur in path[:-1]:
        links = roads[cur].links
        next_link = [link for link in links if link.target == path[cur + 1]][0]
        overall_time += compute_time(next_link)
    return overall_time

# heuristic time to reach the target junction from the src junction
def heuristic_time(roads, src, target):
    src_lat = roads[src].lat
    src_lon = roads[src].lon
    target_lat = roads[target].lat
    target_lon = roads[target].lon

    # use the speed as the average speed since we don't have a given road type
    speed = sum(maxspeeds) / len(maxspeeds)
    return compute_distance(src_lat, src_lon, target_lat, target_lon) / speed