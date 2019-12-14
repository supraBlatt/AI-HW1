'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple, Counter
from ways import load_map_from_csv

def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])

    # save the junctions and links in lists for calculations
    distances = []
    type_counter = Counter()
    link_count = []

    for junction in roads.junctions():
        link_count.append(len(junction.links))

    for link in roads.iterlinks():
        distances.append(link.distance)
        type_counter[link.highway_type] += 1

    return {

        # count the junctions and the links brainded
        'Number of junctions' : len(roads),
        'Number of links' : sum(link_count),
        'Outgoing branching factor' : Stat(max=max(link_count),
                                           min=min(link_count),
                                           avg=sum(link_count)/len(link_count)),
        'Link distance' : Stat(max=max(distances),
                               min=min(distances),
                               avg=sum(distances)/len(distances)),

        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : {k: type_counter[k] for k in sorted(type_counter)}  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
