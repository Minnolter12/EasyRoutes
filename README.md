## EasyRoutes
This is a campus navigation map project based on the A* Algorithm, modeled on Amrita Vishwa Vidyapeetham, Coimbatore.
The algorithm finds the shortest and most efficient path from a start landmark to a goal landmark using lowest cost calculated by the Python A* algorithm.

### Usage

#### 1. Interactive Web Map (Frontend + Python Backend)
Run the Python backend server:
```bash
python3 easyroutes.py
# or: python3 server.py
# or: python3 easyroutes.py --serve --port 8000
```
Then open your browser and navigate to:
```
http://localhost:8000
```
The frontend (`index.html`) communicates directly with the Python backend API endpoint (`/api/route`) to execute `easyRoute()` in `easyroutes.py`.

#### 2. CLI Shortest Path Finder
Find the shortest path directly from the command line:
```bash
python3 easyroutes.py --start E --goal J
```

Output:
```
Shortest path: E -> G -> J
Total distance: 606 meters
```

#### 3. Visual Plot
Generate a 2D scatter plot of campus landmark coordinates:
```bash
python3 plots.py
```
