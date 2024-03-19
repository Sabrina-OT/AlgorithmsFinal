import networkx as nx
import matplotlib.pyplot as plt
import csv

# Load data from CSV file
def load_network_from_csv(filename):
    G = nx.DiGraph()  # Use DiGraph to create a weighted directed graph
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            node = row[0]
            if not node:  # Skip rows where the node is empty
                continue
            connections = []
            distances = []
            for i in range(1, len(row), 2):
                if row[i]:  # Skip empty connections
                    connections.append(row[i])
                    if i + 1 < len(row) and row[i + 1]:  # Skip empty distances
                        distances.append(int(row[i + 1]))
                    else:
                        distances.append(None)
            for neighbor, distance in zip(connections, distances):
                if neighbor:  # Skip adding edges if neighbor node is empty
                    G.add_edge(node, neighbor, weight=distance)

    return G

# Example usage
filename = 'network_data.csv'
network_graph = load_network_from_csv(filename)

# Draw the graph
pos = nx.kamada_kawai_layout(network_graph, scale=2)  # Adjust the scale parameter
nx.draw(network_graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(network_graph, 'weight')
nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=edge_labels)

plt.title('Weighted Directed Graph (Kamada-Kawai layout)')
plt.show()
