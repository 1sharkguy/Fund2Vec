import pandas as pd
import numpy as np
import networkx as nx
from gensim.models import Word2Vec
from sklearn.metrics import v_measure_score
from sklearn.metrics.pairwise import cosine_similarity

# Load the data
file_path = 'combined_fund_data.csv'
data = pd.read_csv(file_path)

# Transform the data into long format for network construction
data_long = data.melt(id_vars=['Fund Name'], var_name='Asset', value_name='Weight')
data_long = data_long[data_long['Weight'] > 0]

# Create the bipartite graph
B = nx.Graph()
funds = data_long['Fund Name'].unique()
assets = data_long['Asset'].unique()
B.add_nodes_from(funds, bipartite=0)
B.add_nodes_from(assets, bipartite=1)
B.add_weighted_edges_from(data_long.values)

# Project the bipartite graph to one-mode graph (only funds)
fund_graph = nx.bipartite.weighted_projected_graph(B, funds)

# Custom Node2Vec implementation using gensim
def custom_node2vec(graph, dimensions=16, walk_length=30, num_walks=200, workers=4):
    walks = []
    nodes = list(graph.nodes())
    for _ in range(num_walks):
        np.random.shuffle(nodes)
        for node in nodes:
            walk = [node]
            while len(walk) < walk_length:
                cur = walk[-1]
                neighbors = list(graph.neighbors(cur))
                if len(neighbors) > 0:
                    walk.append(np.random.choice(neighbors))
                else:
                    break
            walks.append(walk)
    model = Word2Vec(walks, vector_size=dimensions, window=10, min_count=1, sg=1, workers=workers)
    return model

# Fit the custom Node2Vec model
model = custom_node2vec(fund_graph, dimensions=16, walk_length=64, num_walks=128, workers=4)

# Get embeddings for all funds
embeddings = {str(node): model.wv[str(node)] for node in fund_graph.nodes}

# Calculate cosine similarity matrix for all funds in the original high-dimensional space
fund_names = data['Fund Name'].tolist()
original_vectors = data.drop('Fund Name', axis=1).values
original_cos_sim_matrix = cosine_similarity(original_vectors)

# Calculate cosine similarity matrix for all funds in the low-dimensional embedding space
embedding_vectors = np.array([embeddings[fund] for fund in fund_names])
embedding_cos_sim_matrix = cosine_similarity(embedding_vectors)

# Convert the cosine similarity matrices to DataFrames
original_cos_sim_df = pd.DataFrame(original_cos_sim_matrix, index=fund_names, columns=fund_names)
embedding_cos_sim_df = pd.DataFrame(embedding_cos_sim_matrix, index=fund_names, columns=fund_names)

# Save the DataFrame to a CSV file
output_file_path = 'cosine_similarity_funds.csv'
embedding_cos_sim_df.to_csv(output_file_path)

print(f"Cosine similarity matrix saved to {output_file_path}")

# Function to calculate Jaccard index
def jaccard_index(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

# Calculate Jaccard indices for top-k similar funds
def calculate_jaccard_indices(original_sim_df, embedding_sim_df, k):
    jaccard_indices = []
    for fund in original_sim_df.index:
        original_top_k = set(original_sim_df[fund].nlargest(k + 1).index) - {fund}
        embedding_top_k = set(embedding_sim_df[fund].nlargest(k + 1).index) - {fund}
        jaccard_indices.append(jaccard_index(original_top_k, embedding_top_k))
    return np.mean(jaccard_indices)

# Calculate Jaccard index for different values of k
k_values = [5, 10, 20, 50]
jaccard_results = {k: calculate_jaccard_indices(original_cos_sim_df, embedding_cos_sim_df, k) for k in k_values}

print("Jaccard Index results:")
for k, jaccard in jaccard_results.items():
    print(f"Top-{k} similar funds: {jaccard}")
