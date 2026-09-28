import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import powerlaw
import pandas as pd
import itertools
import pickle

# 参数设置
initial_infected_ratio = 0.01
num_nodes = 4941

#信息层参数
lambda_info = 0.24  # 只考虑单纯形
lambda_star = 0.24
alpha = 10
theta = 0.3
delta = 0.5

#物理层参数
mu = 0.4
beta_A = 0.0  # 感知状态下对疾病免疫

# # 固定种子以保证每次生成相同的图和2-单纯形
# seed_value = 211
# random.seed(seed_value)
# # 生成ER图
# G_info = nx.erdos_renyi_graph(4941, p=6/4936, seed=seed_value)
# # 2-单纯形概率
# prob_2_simplex = 1 * 4 / (4940 * 4939) # k=2
# # 用于保存构造的2-单纯形
# simplices_2 = []
# # 用于保存每个节点的2-单纯形邻居
# node_simplex_neighbors = {node: [] for node in G_info.nodes}
# # 遍历所有的三元节点组合(i, j, k)
# nodes = list(G_info.nodes)
# for i, j, k in itertools.combinations(nodes, 3):
#     if random.random() < prob_2_simplex:
#         # 如果三者之间的边不存在，则添加
#         if not G_info.has_edge(i, j):
#             G_info.add_edge(i, j)
#         if not G_info.has_edge(i, k):
#             G_info.add_edge(i, k)
#         if not G_info.has_edge(j, k):
#             G_info.add_edge(j, k)
#         # 保存2-单纯形
#         simplices_2.append((i, j, k))
#         # 更新节点的2-单纯形邻居信息
#         node_simplex_neighbors[i].append((j, k))
#         node_simplex_neighbors[j].append((i, k))
#         node_simplex_neighbors[k].append((i, j))
#
# a_matrix = nx.to_numpy_array(G_info)
# # 输出构造的2-单纯形的数量
# print(f"Number of 2-simplices constructed: {len(simplices_2)}")

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

# 物理层， 定义文件路径
file_path = "./out.opsahl-powergrid_reindexed"
# 初始化无向图
G_epidemic = nx.Graph()
# 读取文件并构建图
with open(file_path, 'r') as f:
    for line in f:
        # 读取每行数据，假设以空格分隔节点编号
        nodes = line.strip().split()
        if len(nodes) == 2:
            u, v = nodes
            G_epidemic.add_edge(int(u), int(v))

b_matrix = nx.to_numpy_array(G_epidemic)

#找信息和物理层邻居
def get_neighbors(G, node):
    return list(G.neighbors(node))

#求r_i_1
def get_r_i_1(a_matrix, P_A):
     return np.prod(1 - a_matrix * P_A[:, None] * lambda_info, axis=0)


def get_r_i_2(node_simplex_neighbors, P_A, lambda_star):
    num_nodes = len(P_A)
    r_i_2 = np.ones(num_nodes)
    for i in range(num_nodes):
        product = 1
        for (j, k) in node_simplex_neighbors[i]:
            # 对于每个与 i 共同构成 2-单纯形的 (j, k) 节点对
            c_ijk = P_A[j] * P_A[k]
            product *= (1 - c_ijk * lambda_star)

        r_i_2[i] = product

    return r_i_2

def get_r_i_3(b_matrix, P_AI, theta):
    num_nodes = b_matrix.shape[0]
    r_i_3 = np.ones(num_nodes)
    for i in range(num_nodes):
        k_i = np.sum(b_matrix[i])  # 节点 i 在物理层的邻居数
        sum_bji_Pj = np.sum(b_matrix[i] * P_AI)  # ∑_{j} b_{ji} P_{j}^{AI}
        fraction = sum_bji_Pj / k_i if k_i > 0 else 0  # ∑_{j} b_{ji} P_{j}^{AI} / k_i
        #r_i_3[i] = np.heaviside(theta - proportion, 1)  # 当 proportion >= theta 时返回 1，否则返回 0
        r_i_3[i] = 1-1 / (1 + np.exp(-alpha * (fraction-theta)))  # np.exp(-theta * proportion)

    return r_i_3

def get_q_i(b_matrix, P_AI, beta):
    return np.prod(1 - b_matrix * P_AI[:, None] * beta, axis=0)

# 迭代更新节点状态概率的函数
def iterate_probabilities(beta_U):
    # 初始化节点状态概率
    P_AI = np.zeros(num_nodes)
    P_AS = np.zeros(num_nodes)
    P_US = np.ones(num_nodes)  # 初始时所有节点均为US状态
    initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
    P_AI[initial_infected] = 1
    P_US[initial_infected] = 0

    # 迭代更新节点状态概率
    max_iterations = 10000
    tolerance = 1e-6

    for iteration in range(max_iterations):
        P_A = P_AI + P_AS
        r_i = get_r_i_2(node_simplex_neighbors, P_A, lambda_star) * get_r_i_1(a_matrix, P_A)  * get_r_i_2(node_simplex_neighbors, P_A, lambda_star) * get_r_i_3(b_matrix, P_AI, theta)
        q_i_A = get_q_i(b_matrix, P_AI, beta_A)
        q_i_U = get_q_i(b_matrix, P_AI, beta_U)

        P_US_next = P_AI * delta * mu + P_US * r_i * q_i_U + P_AS * delta * q_i_U
        P_AS_next = P_AI * (1 - delta) * mu + P_US * (1 - r_i) * q_i_A + P_AS * (1 - delta) * q_i_A
        P_AI_next = P_AI * (1 - mu) + P_US * ((1 - r_i) * (1 - q_i_A) + r_i * (1 - q_i_U)) + P_AS * (
                    delta * (1 - q_i_U) + (1 - delta) * (1 - q_i_A))

        # 检查收敛性
        if np.max(np.abs(P_US_next - P_US)) < tolerance and np.max(np.abs(P_AS_next - P_AS)) < tolerance and np.max(
                np.abs(P_AI_next - P_AI)) < tolerance:
            break
        P_US, P_AS, P_AI = P_US_next, P_AS_next, P_AI_next

    # 计算感染密度和感知密度
    infection_density = np.mean(P_AI)
    awareness_density = np.mean(P_A)
    return infection_density, awareness_density

#  ###主函数，遍历 beta_U 值，得到感染密度
beta_U_values = np.arange(0, 1.02, 0.02)
infection_densities = []
awareness_densities = []
for beta_U in beta_U_values:
    print("beta_u", beta_U)
    # 保存 def iterate_probabilities(beta_U)得到的感染密度
    infection_density, awareness_density = iterate_probabilities(beta_U)
    infection_densities.append(infection_density)
    awareness_densities.append(awareness_density)

# 保存数据到 CSV 文件
data = {
    'beta_U': beta_U_values,
    'infection_density': infection_densities,
    'awareness_density': awareness_densities
}
df = pd.DataFrame(data)
df.to_csv('k=2MMCA理论密度822.csv', index=False)

# 绘制结果
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(beta_U_values, awareness_densities, marker='o')
plt.title('Aware Nodes Ratio vs. β_U')
plt.xlabel('β_U')
plt.xlim(0, 1)
plt.ylim(0,)
plt.ylabel('Aware Nodes Ratio')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(beta_U_values, infection_densities, marker='o')
plt.title('Infected Nodes Ratio vs. β_U')
plt.xlabel('β_U')
plt.xlim(0, 1)
plt.ylim(0,)
plt.ylabel('Infected Nodes Ratio')
plt.grid(True)

plt.tight_layout()
plt.show()


