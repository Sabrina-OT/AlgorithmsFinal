# Implement Dijkstra's algorithm to determine the shortest path from the 
# starting node to each charging station. This will show all the possible 
# shortest paths for all four-charging station from a starting point 

import csv
import heapq

# Function to read the graph data from the CSV file
def read_graph(filename):
    graph = {}

    #encoding portion removes problem with additional characters added to CSV file
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)

        # Iterate through each row of the CSV file
        for row in reader:
            # Extract the node from the first element (the node)
            node = row[0]
            neighbors = {}

            # Iterate through the rest of the row by steps of 2
            for i in range(1, len(row), 2):
                # Check if the empty
                if row[i] != '':
                    # Add the neighbor and its weight to the neighbors dictionary
                    neighbors[row[i]] = int(row[i + 1])
            # Add the node and its neighbors to the graph dictionary
            graph[node] = neighbors

    return graph

# Dijkstra's algorithm to find the shortest paths from a starting node to all nodes
def dijkstra(graph, start):

    # Initialize a dictionary to store the shortest path distances
    distances = {node: float('inf') for node in graph}
    # Set the distance from the starting node to 0
    distances[start] = 0
    # Create an empty set to store the visited node
    visited = set()
    # Create a priority queue to store nodes to be visited next
    PriorityQueue = [(0, start)]
    
    # Loop until each node has been visited
    while PriorityQueue:
        # Pop the node with the shortest distance from the PriorityQueue
        distance, current_node = heapq.heappop(PriorityQueue)
        
        if current_node in visited:
            continue
        # Mark the current node as visited
        visited.add(current_node)

        # Iterate through the neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                # Calculate the new distance to the neighbor node
                new_distance = distance + weight
                
                # If the new distance is shorter than the current shorests distance, update
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    # Add the neighbor to the priorty queue with its new distance
                    heapq.heappush(PriorityQueue, (new_distance, neighbor))
    
    return distances

# Main function
def main():
    filename = 'network_data.csv' 
    start_node = 'A'
    graph = read_graph(filename)

    distances = dijkstra(graph, start_node)

    # THIS SECTION SHOULD BE DELETED LATER, BUT KEEP FOR NOW PLS----------
    print("\nDistance to all the nodes")
    print("Shortest paths from node", start_node)
    for node, distance in distances.items():
        print("To node", node, ":", distance)
    # --------------------------------------------------------------------
        
    print("\nWe only care about these:")
    print("Shortest paths from node", start_node)
    print()
    for node, distance in distances.items():
        if node in ['H', 'K', 'O', 'T']:  # Only consider required nodes
            print("Distance to Gas Station", node, ":", distance)
            #print("To node", node, ":", distance)

if __name__ == "__main__":
    main()
