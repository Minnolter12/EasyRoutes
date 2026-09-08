from math import sqrt, pow

nodes: dict = {
    # Actual nodes of real locations, represented
    #  as coordinates in a cartesian system
    'A': (0, 277),      # Vasishta
    'B': (162, 504),    # AB2
    'C': (345, 541),    # Library
    'D': (410, 429),    # Gargi bhavanam
    'E': (634, 572),    # ASB / Canteen / Pandal
    'F': (994, 421),    # Kashyapa
    'G': (627, 295),    # General store / PE building
    'H': (580, 157),    # Mythreyi bhavanam
    'I': (748, 115),    # AB1
    'J': (854, 151),    # Sopanam
    'K': (454, 0)       # Main Gate
}

graph: dict = {
    # Distances from various nodes
    'A' : {'B' : 432},
    'B' : {'C' : 92, 'D' : 320, 'A' : 432},
    'C' : {'B' : 92, 'E' : 287},
    'D' : {'K' : 432, 'G' : 319, 'B' : 320},
    'E' : {'G' : 278, 'F' : 432, 'C' : 287},
    'F' : {'J' : 455, 'G' : 420, 'E' : 432 },
    'G' : {'D' : 319, 'J' : 328, 'F' : 420, 'E' : 278},
    'H' : {'K' : 269 , 'I' : 397},
    'I' : {'J' : 215, 'H' : 397},
    'J' : {'F' : 455, 'G' : 328, 'I': 215},
    'K' : {'D' : 432, 'H' : 269}
}


def euclidianDistance(nodes: dict, nodeOne, nodeTwo) -> int:
    try:
        x1_cordinate = nodes[nodeOne][0]
        y1_cordinate = nodes[nodeOne][1]

        x2_cordinate = nodes[nodeTwo][0]
        y2_cordinate = nodes[nodeTwo][1]

        return abs(
            sqrt(
                pow((x1_cordinate - x2_cordinate), 2) +
                pow((y1_cordinate - y2_cordinate), 2)
            )
        )

    except KeyError as e:
        print(f"Error: Node {e} does not exist in dict")
        return None

    except TypeError:
        print(f"Coordinates must be numbers!")
        return None

    





