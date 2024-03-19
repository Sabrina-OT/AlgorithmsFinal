import networkx as nx
import matplotlib.pyplot as plt
import csv

# Load data from CSV file
def load_network_from_csv(filename):
    G = nx.Graph()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header (first row)
        for row in reader:
            node = row[0]
            connections = row[1::2]  # Extracting every other element starting from index 1
            distances = []
            for distance_str in row[2::2]:
                if distance_str:
                    distances.append(int(distance_str))
                else:
                    distances.append(0)
            for neighbor, distance in zip(connections, distances):
                G.add_edge(node, neighbor, weight=distance)

    return G

# Example usage
filename = 'network_data.csv'
network_graph = load_network_from_csv(filename)

# Draw the graph
pos = nx.kamada_kawai_layout(network_graph)  # Specify layout algorithm (Kamada-Kawai layout)
nx.draw(network_graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(network_graph, 'weight')
nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=edge_labels)

plt.title('Network Graph (Kamada-Kawai layout)')
plt.show()
