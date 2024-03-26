# Implement Dijkstra's algorithm to determine the shortest path from the 
# starting node to each charging station. This will show all the possible 
# shortest paths for all four-charging station from a starting point 

import csv
import heapq

# Function to read the graph data from the CSV file
def read_graph(filename):
    graph = {}
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            node = row[0]
            neighbors = {}
            for i in range(1, len(row), 2):
                if row[i] != '':
                    neighbors[row[i]] = int(row[i + 1])
            graph[node] = neighbors
    return graph

# Dijkstra's algorithm to find the shortest paths from a starting node to all nodes
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    pq = [(0, start)]
    
    while pq:
        distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)
        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                new_distance = distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(pq, (new_distance, neighbor))
    
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
    for node, distance in distances.items():
        if node in ['H', 'K', 'O', 'T']:  # Only consider required nodes
            print("To node", node, ":", distance)


    

if __name__ == "__main__":
    main()
