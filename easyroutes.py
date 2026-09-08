from math import sqrt, pow
import heapq
import argparse

nodes = {
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


graph = {
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


def euclidianDistance(nodes, nodeOne, nodeTwo) -> int:
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
    

def easyRoute(startNode, goalNode, graph, nodes) -> None:
    open_set = []

    heapq.heappush(
        open_set, 
        (euclidianDistance(nodes, startNode, goalNode), 0, startNode)
    )

    came_from = {}
    g_scores = {startNode: 0}
                   
    while open_set:
        # unpack the tuple 
        heuristic_value, g, currentNode = heapq.heappop(open_set)

        # check if goal node is reached
        if currentNode == goalNode:
            path = []
            curr = goalNode
            while curr in came_from:
                path.append(curr)
                curr = came_from[curr]
            path.append(startNode)
            path.reverse()
            return path, g

        # 2. Skip outdated entries in the heap
        if g > g_scores.get(currentNode, float('inf')):
            continue

        # if goal node is not reached, get the neighbours
        for neighbour, roadDistance in graph[currentNode].items():
            totalDistance = g + roadDistance
            
            if totalDistance < g_scores.get(neighbour, float('inf')):
                g_scores[neighbour] = totalDistance
                came_from[neighbour] = currentNode

                hVal = euclidianDistance(nodes, neighbour, goalNode)
                finalScore = totalDistance + hVal

                heapq.heappush(open_set, (finalScore, totalDistance, neighbour))


def main():
    parser = argparse.ArgumentParser(description="Find the shortest path on campus using A*.")
    
    parser.add_argument("--start", "-s", required=True, help="Starting node (e.g., E)")
    parser.add_argument("--goal", "-g", required=True, help="Goal node (e.g., J)")
    
    args = parser.parse_args()

    start_node = args.start.upper()
    goal_node = args.goal.upper()

    # Validate node existence
    if start_node not in nodes or goal_node not in nodes:
        print("Error: Both start and goal nodes must exist in the campus map.")
        return

    result = easyRoute(start_node, goal_node, graph, nodes)

    if result:
        path, distance = result
        print(f"Shortest path: {' -> '.join(path)}")
        print(f"Total distance: {distance} meters")
    else:
        print(f"No path found between {start_node} and {goal_node}.")

if __name__ == "__main__":
    main()