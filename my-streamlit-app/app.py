import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Graph, Use Case: Emergency Supply Robot

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}

# Heuristic
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.hypot(x2 - x1, y2 - y1)

# Path reconstruction
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# GBFS
def gbfs(start, goal):
    came_from = {}
    visited = []
    open_set = [(heuristic(start, goal), start)]

    while open_set:
        h, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.append(current)

        if current == goal:
            break

        for neighbor, cost in hospital_graph[current].items():
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))

    if goal not in visited:
        return None, None

    path = reconstruct_path(came_from, goal)
    cost = sum(hospital_graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
    return path, cost

# A*
def a_star(start, goal):
    came_from = {}
    g_cost = {start: 0}
    visited = []
    open_set = [(heuristic(start, goal), start)]

    while open_set:
        f, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.append(current)

        if current == goal:
            break

        for neighbor, cost in hospital_graph[current].items():
            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    if goal not in g_cost:
        return None, None

    path = reconstruct_path(came_from, goal)
    return path, g_cost[goal]

##########################################
# Streamlit GUI Code

# Set Page Config
st.set_page_config(page_title="Emergency Supply Robot", layout="centered")

# write meaningful title and description for the app
st.title("🏥 Emergency Supply Robot Pathfinder")
st.write("Pick a start and goal location, then compare GBFS vs A* routes through the hospital.")

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)

if st.button("Run Search"):

    if algorithm == "GBFS":
        # run the GBFS algorithm with the selected start and goal nodes
        path, cost = gbfs(start, goal)
    else:
        # run the A* algorithm with the selected start and goal nodes
        path, cost = a_star(start, goal)

    if path is None:
        # display a error message indicating that no path was found
        st.error("No path found between the selected nodes.")

    else:

        # Display result
        st.subheader("Search Result")

        st.write(
            f"Algorithm: {algorithm}"
        )

        st.write(
            f"Solution Path: {' → '.join(path)}"
        )

        st.write(
            f"Total Path Cost: {cost:.2f}"
        )

        # Visualize NetworkX graph

        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        # WRITE REMAINING NETWORKX VISUALIZATION CODE HERE
        nx.draw(G, pos, ax=ax, with_labels=True, node_color="lightblue",
                node_size=1800, font_size=8, font_weight="bold")
        nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=15)

        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges,
                                width=3, arrows=True, arrowsize=20, edge_color="red")

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)