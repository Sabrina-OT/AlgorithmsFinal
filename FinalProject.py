# Import necessary libraries
import csv  # Library for reading CSV files
import networkx as nx  # Library for working with graphs
import matplotlib.pyplot as plt  # Library for plotting graphs
from tkinter import messagebox  # Library for displaying message boxes

# Function to read the graph data from the CSV file
def read_graph(filename):
    graph = {}  # Initialize an empty dictionary to store the graph data

    # Open the CSV file and read its contents
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)  # Create a CSV reader object

        # Iterate through each row of the CSV file
        for row in reader:
            # Extract the node from the first element of the row
            node = row[0]
            neighbors = {}  # Initialize an empty dictionary to store the node's neighbors

            # Iterate through the rest of the row by steps of 2
            for i in range(1, len(row), 2):
                # Check if the entry is not empty
                if row[i] != '':
                    # Add the neighbor and its weight to the neighbors dictionary
                    neighbors[row[i]] = int(row[i + 1])

            # Add the node and its neighbors to the graph dictionary
            graph[node] = neighbors

    return graph

# Dijkstra's algorithm to find the shortest paths from a starting node to all nodes
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}  # Initialize distances to all nodes as infinity
    distances[start] = 0  # Set the distance to the starting node as 0
    visited = set()  # Initialize an empty set to keep track of visited nodes
    PriorityQueue = [(0, start)]  # Initialize a priority queue with the starting node and its distance
    
    # Iterate until the priority queue is empty
    while PriorityQueue:
        distance, current_node = PriorityQueue.pop(0)  # Extract the node with the shortest distance from the priority queue
        
        if current_node in visited:  # Skip the node if it has already been visited
            continue
        
        visited.add(current_node)  # Mark the current node as visited
        
        if current_node not in graph:  # Skip nodes not in the graph
            continue  # Skip nodes not in the graph
        
        # Iterate through the neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:  # Process unvisited neighbors
                new_distance = distance + weight  # Calculate the new distance to the neighbor
                
                # Update the distance if the new distance is shorter than the current distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance  # Update the distance to the neighbor
                    PriorityQueue.append((new_distance, neighbor))  # Add the neighbor to the priority queue
    
    return distances  # Return the shortest distances to all nodes from the starting node

# Function to highlight the shortest paths to gas stations
def highlight_shortest_paths(G, start_node, gas_stations):
    # Find all shortest paths from the starting node to each gas station
    paths = nx.single_source_shortest_path(G, start_node)
    shortest_paths = []
    
    # Iterate through the gas stations
    for station in gas_stations:
        if station in paths:  # Check if a path exists to the gas station
            shortest_paths.append(nx.shortest_path(G, start_node, station))  # Add the shortest path to the list of shortest paths
    
    # Create a subgraph containing nodes along the shortest paths
    H = G.subgraph([node for path in shortest_paths for node in path])
    
    return H, shortest_paths  # Return the subgraph and the list of shortest paths

# Main function
def main():
    filename = 'network_data.csv'  # Path to the CSV file containing the graph data

    # Read full graph
    graph = read_graph(filename)

    # Create a graph from the network data with weighted edges
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    # Create a text box for the title on the first graph
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.text(0.5, 1.05, "EV Charging Station Route Optimization Application",
            horizontalalignment='center', verticalalignment='center',
            fontsize=16, fontweight='bold', transform=ax.transAxes)
    ax.axis('off')
    
    # Draw the full graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=12, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
    plt.tight_layout()
    plt.show()

    # Prompt user to input starting node
    start_node = input("Enter starting node: ").upper()

    # Check if starting node is valid
    if start_node not in graph:
        messagebox.showerror("Error", "Invalid starting node.")
        return

    # Find gas stations
    gas_stations = ['H', 'K', 'O', 'T']

    # Highlight shortest paths
    H, shortest_paths = highlight_shortest_paths(G, start_node, gas_stations)

    # Create a new figure for the second graph
    plt.figure(figsize=(10, 8))

    # Create a text box for the title on the second graph
    ax = plt.gca()
    ax.text(0.5, 1.05, "Best path from {}".format(start_node),
            horizontalalignment='center', verticalalignment='center',
            fontsize=16, fontweight='bold', transform=ax.transAxes)
    ax.axis('off')
   

    # Draw the graph with highlighted shortest paths
    node_colors = ['yellow' if node == start_node else 'orange' if node in gas_stations else 'lightgreen' for node in H.nodes()]  # Highlight starting node and gas stations
    nx.draw(H, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=12, edge_color='gray')
    nx.draw_networkx_edge_labels(H, pos, edge_labels={(u, v): d['weight'] for u, v, d in H.edges(data=True)})

    # Define colors for arrows
    colors = ['red', 'blue', 'green', 'purple']

    # Add arrows to indicate direction from start_node to gas stations
    for i, station in enumerate(gas_stations):
        if nx.has_path(H, start_node, station):
            path = shortest_paths[i]
            for j in range(len(path) - 1):
                offset = 0.05 * (j + 1)
                plt.annotate("", xy=pos[path[j + 1]], xytext=pos[path[j]],
                            arrowprops=dict(arrowstyle="->", color=colors[i], connectionstyle=f"arc3,rad={offset}"))

    # Add labels for the total distance of each shortest path
    for i, path in enumerate(shortest_paths):
        total_distance = sum(G[path[j]][path[j+1]]['weight'] for j in range(len(path) - 1))
        node_pos = pos[path[-1]]
        plt.text(node_pos[0], node_pos[1] + 0.1, f"Total Distance: {total_distance}", ha='center', va='center', fontsize=10, fontweight='bold', bbox=dict(facecolor='white', edgecolor='white'))

    plt.axis('off')  # Turn off axis labels and ticks
    plt.tight_layout()  # Adjust layout
    plt.show()  # Display the plot




if __name__ == "__main__":
    main()
