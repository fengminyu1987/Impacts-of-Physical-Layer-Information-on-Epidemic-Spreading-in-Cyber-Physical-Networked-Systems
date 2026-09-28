import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import powerlaw
import pandas as pd
import itertools
import pickle

# 固定种子以保证每次生成相同的图和2-单纯形
node_num =4941
seed_value = 211
random.seed(seed_value)
# 生成ER图
G_info = nx.erdos_renyi_graph(node_num, p=4.005/(node_num-5), seed=seed_value)
# 2-单纯形概率
prob_2_simplex = 1 * 2.67 / ((node_num-1) * (node_num-2)) # k=2
# 用于保存构造的2-单纯形
simplices_2 = []
# 用于保存每个节点的2-单纯形邻居
node_simplex_neighbors = {node: [] for node in G_info.nodes}
# 遍历所有的三元节点组合(i, j, k)
nodes = list(G_info.nodes)
for i, j, k in itertools.combinations(nodes, 3):
    if random.random() < prob_2_simplex:
        # 如果三者之间的边不存在，则添加
        if not G_info.has_edge(i, j):
            G_info.add_edge(i, j)
        if not G_info.has_edge(i, k):
            G_info.add_edge(i, k)
        if not G_info.has_edge(j, k):
            G_info.add_edge(j, k)
        # 保存2-单纯形
        simplices_2.append((i, j, k))
        # 更新节点的2-单纯形邻居信息
        node_simplex_neighbors[i].append((j, k))
        node_simplex_neighbors[j].append((i, k))
        node_simplex_neighbors[k].append((i, j))


# 保存 G_info 和 simplices_2
with open("graph_data.pkl", "wb") as f:
    pickle.dump((G_info, simplices_2, node_simplex_neighbors), f)
print("Graph and simplices_2 saved successfully!")

# 加载保存的数据
with open("graph_data.pkl", "rb") as f:
    G_info, simplices_2, node_simplex_neighbors = pickle.load(f)

print("Graph and simplices_2 loaded successfully!")

# 输出 G_info 中的节点数和边数
print(f"节点数: {len(G_info.nodes)}")
print(f"边数: {len(G_info.edges)}")

# 输出 simplices_2 中的单纯形个数
print(f"2-单纯形个数: {len(simplices_2)}")

a_matrix = nx.to_numpy_array(G_info)