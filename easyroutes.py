from math import sqrt, pow
import heapq
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import json
import os
import sys

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


class EasyRoutesHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler serving both static frontend files (index.html)
    and REST API endpoints that execute the Python A* algorithm (easyRoute).
    """

    def end_headers(self):
        # Enable CORS for local development across different origins/ports
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # A* Route computation endpoint: /api/route?start=E&goal=J
        if parsed.path == "/api/route":
            params = urllib.parse.parse_qs(parsed.query)
            start_list = params.get("start")
            goal_list = params.get("goal")

            if not start_list or not goal_list:
                self._send_json({"error": "Missing 'start' or 'goal' parameter."}, status=400)
                return

            start_node = start_list[0].upper().strip()
            goal_node = goal_list[0].upper().strip()

            if start_node not in nodes or goal_node not in nodes:
                self._send_json({
                    "error": f"Invalid node(s): start='{start_node}', goal='{goal_node}'."
                }, status=400)
                return

            # Execute user's Python A* algorithm
            result = easyRoute(start_node, goal_node, graph, nodes)
            if result:
                path, distance = result
                segments = []
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    seg_dist = graph.get(u, {}).get(v, None)
                    segments.append({"from": u, "to": v, "distance": seg_dist})

                self._send_json({
                    "success": True,
                    "engine": "python_easyroutes",
                    "start": start_node,
                    "goal": goal_node,
                    "path": path,
                    "distance": distance,
                    "segments": segments
                })
            else:
                self._send_json({
                    "success": False,
                    "error": f"No path found between {start_node} and {goal_node}."
                }, status=404)
            return

        # Health/status check endpoint: /api/health
        if parsed.path == "/api/health":
            self._send_json({
                "status": "ok",
                "backend": "easyroutes.py",
                "algorithm": "A*",
                "nodes_count": len(nodes)
            })
            return

        # Campus nodes data endpoint: /api/nodes
        if parsed.path == "/api/nodes":
            self._send_json({
                "nodes": {k: {"x": v[0], "y": v[1]} for k, v in nodes.items()}
            })
            return

        # Campus road graph endpoint: /api/graph
        if parsed.path == "/api/graph":
            self._send_json({"graph": graph})
            return

        # Default: serve index.html and static files from the project directory
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/route":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
            except Exception:
                self._send_json({"error": "Invalid JSON in request body."}, status=400)
                return

            start_node = str(data.get("start", "")).upper().strip()
            goal_node = str(data.get("goal", "")).upper().strip()

            if not start_node or not goal_node:
                self._send_json({"error": "Missing 'start' or 'goal' in request body."}, status=400)
                return

            if start_node not in nodes or goal_node not in nodes:
                self._send_json({
                    "error": f"Invalid node(s): start='{start_node}', goal='{goal_node}'."
                }, status=400)
                return

            result = easyRoute(start_node, goal_node, graph, nodes)
            if result:
                path, distance = result
                segments = []
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    seg_dist = graph.get(u, {}).get(v, None)
                    segments.append({"from": u, "to": v, "distance": seg_dist})

                self._send_json({
                    "success": True,
                    "engine": "python_easyroutes",
                    "start": start_node,
                    "goal": goal_node,
                    "path": path,
                    "distance": distance,
                    "segments": segments
                })
            else:
                self._send_json({
                    "success": False,
                    "error": f"No path found between {start_node} and {goal_node}."
                }, status=404)
            return

        self._send_json({"error": "Endpoint not found."}, status=404)

    def _send_json(self, data, status=200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def log_message(self, format, *args):
        sys.stderr.write(f"[easyroutes.py backend] {format % args}\n")


def run_server(host="0.0.0.0", port=8000):
    server_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(server_dir)

    server_address = (host, port)
    httpd = HTTPServer(server_address, EasyRoutesHandler)
    display_host = "localhost" if host in ("0.0.0.0", "") else host
    print("==================================================")
    print(" 🚀 EasyRoutes Backend Server Running!            ")
    print(f" 🌐 Web Frontend: http://{display_host}:{port}/     ")
    print(f" ⚙️ A* Route API: http://{display_host}:{port}/api/route")
    print("==================================================")
    print("Press Ctrl+C to stop the server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping EasyRoutes backend server...")
        httpd.server_close()
        print("Server stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="Amrita Campus Navigation: CLI A* pathfinder and Backend Web Server."
    )
    
    parser.add_argument("--start", "-s", required=False, help="Starting node (e.g., E)")
    parser.add_argument("--goal", "-g", required=False, help="Goal node (e.g., J)")
    parser.add_argument("--serve", action="store_true", help="Start the backend HTTP server for index.html")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host (default: 0.0.0.0)")
    
    args = parser.parse_args()

    # CLI pathfinding mode
    if args.start and args.goal:
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
        return

    # Check partial CLI arguments
    if (args.start and not args.goal) or (args.goal and not args.start):
        print("Error: Both --start (-s) and --goal (-g) must be provided for CLI mode.")
        print("Example: python3 easyroutes.py --start E --goal J")
        print("To start the web backend: python3 easyroutes.py --serve (or python3 easyroutes.py)")
        return

    # Default or --serve: Start the backend server
    run_server(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
