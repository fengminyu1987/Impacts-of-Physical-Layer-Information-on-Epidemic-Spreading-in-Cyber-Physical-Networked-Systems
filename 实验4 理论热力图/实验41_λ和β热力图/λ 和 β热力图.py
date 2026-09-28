import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
#
# # 参数设置
# initial_infected_ratio = 0.01
# num_nodes = 1000
#
# # 信息层参数
# lambda_info = None  # lambda_info 会在循环中设置
# delta = 0.8
# lambda_star = 0  # 固定 lambda_star 为 0
# theta = 0  # theta
# alpha = 10
#
# # 物理层参数
# mu = 0.4
# beta_A = 0.0  # 感知状态下对疾病免疫
# #beta_U = 0.5  # 固定 beta_U 值为 0.5
#
# # 固定种子以保证每次生成相同的图和 2-单纯形
# seed_value = 211
# random.seed(seed_value)
# # 生成 ER 图
# G_info = nx.erdos_renyi_graph(num_nodes, p=6/995, seed=seed_value)
#
# # 2-单纯形概率
# prob_2_simplex = 4 / (999 * 998)
# simplices_2 = []
# node_simplex_neighbors = {node: [] for node in G_info.nodes}
# nodes = list(G_info.nodes)
# for i, j, k in itertools.combinations(nodes, 3):
#     if random.random() < prob_2_simplex:
#         if not G_info.has_edge(i, j):
#             G_info.add_edge(i, j)
#         if not G_info.has_edge(i, k):
#             G_info.add_edge(i, k)
#         if not G_info.has_edge(j, k):
#             G_info.add_edge(j, k)
#         simplices_2.append((i, j, k))
#         node_simplex_neighbors[i].append((j, k))
#         node_simplex_neighbors[j].append((i, k))
#         node_simplex_neighbors[k].append((i, j))
#
# a_matrix = nx.to_numpy_array(G_info)
#
# # 生成 2.5 物理层
# G_epidemic = nx.watts_strogatz_graph(num_nodes, 4, 0.5, seed=2)
# b_matrix = nx.to_numpy_array(G_epidemic)
#
# # 找信息和物理层邻居
# def get_neighbors(G, node):
#     return list(G.neighbors(node))
#
# # 求 r_i_1
# def get_r_i_1(a_matrix, P_A):
#     return np.prod(1 - a_matrix * P_A[:, None] * lambda_info, axis=0)
#
# # 求 r_i_2
# def get_r_i_2(node_simplex_neighbors, P_A, lambda_star):
#     num_nodes = len(P_A)
#     r_i_2 = np.ones(num_nodes)
#     for i in range(num_nodes):
#         product = 1
#         for (j, k) in node_simplex_neighbors[i]:
#             c_ijk = P_A[j] * P_A[k]
#             product *= (1 - c_ijk * lambda_star)
#         r_i_2[i] = product
#     return r_i_2
#
# # 求 r_i_3
# def get_r_i_3(b_matrix, P_AI, theta):
#     num_nodes = b_matrix.shape[0]
#     r_i_3 = np.ones(num_nodes)
#     for i in range(num_nodes):
#         k_i = np.sum(b_matrix[i])  # 节点 i 在物理层的邻居数
#         sum_bji_Pj = np.sum(b_matrix[i] * P_AI)  # ∑_{j} b_{ji} P_{j}^{AI}
#         proportion = sum_bji_Pj / k_i if k_i > 0 else 0  # ∑_{j} b_{ji} P_{j}^{AI} / k_i
#         r_i_3[i] = 1 - 1 / (1 + np.exp(-alpha * (proportion - theta)))  # np.exp(-theta * proportion)
#     return r_i_3
#
# # 求 q_i
# def get_q_i(b_matrix, P_AI, beta):
#     return np.prod(1 - b_matrix * P_AI[:, None] * beta, axis=0)
#
# # 迭代更新节点状态概率的函数
# def iterate_probabilities(beta_U):  # 这里限定只传入一个参数
#     # 初始化节点状态概率
#     P_AI = np.zeros(num_nodes)
#     P_AS = np.zeros(num_nodes)
#     P_US = np.ones(num_nodes)  # 初始时所有节点均为US状态
#     initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
#     P_AI[initial_infected] = 1
#     P_US[initial_infected] = 0
#
#     # 迭代更新节点状态概率
#     max_iterations = 10000
#     tolerance = 1e-6
#
#     for iteration in range(max_iterations):
#         P_A = P_AI + P_AS
#         r_i = get_r_i_1(a_matrix, P_A) #  * get_r_i_2(node_simplex_neighbors, P_A, lambda_star) * get_r_i_3(b_matrix, P_AI, theta)
#         q_i_A = get_q_i(b_matrix, P_AI, beta_A)
#         q_i_U = get_q_i(b_matrix, P_AI, beta_U)
#
#         P_US_next = P_AI * delta * mu + P_US * r_i * q_i_U + P_AS * delta * q_i_U
#         P_AS_next = P_AI * (1 - delta) * mu + P_US * (1 - r_i) * q_i_A + P_AS * (1 - delta) * q_i_A
#         P_AI_next = P_AI * (1 - mu) + P_US * ((1 - r_i) * (1 - q_i_A) + r_i * (1 - q_i_U)) + P_AS * (
#                 delta * (1 - q_i_U) + (1 - delta) * (1 - q_i_A))
#
#         # 检查收敛性
#         if np.max(np.abs(P_US_next - P_US)) < tolerance and np.max(np.abs(P_AS_next - P_AS)) < tolerance and np.max(
#                 np.abs(P_AI_next - P_AI)) < tolerance:
#             break
#         P_US, P_AS, P_AI = P_US_next, P_AS_next, P_AI_next
#
#     # 计算感染密度和感知密度
#     infection_density = np.mean(P_AI)
#     awareness_density = np.mean(P_A)
#     return infection_density, awareness_density
#
# # 遍历 lambda_info 和 theta 的值
# lambda_info_values = np.linspace(0, 1, 51)
# beta_values = np.linspace(0, 1, 51)
# infection_density_matrix = np.zeros((len(lambda_info_values), len(beta_values)))
# awareness_density_matrix = np.zeros((len(lambda_info_values), len(beta_values)))
#
# for i, lambda_info in enumerate(lambda_info_values):
#     print('lambda_info:', lambda_info)
#     for j, beta_U in enumerate(beta_values):
#         infection_density, awareness_density = iterate_probabilities(beta_U)
#         infection_density_matrix[i, j] = infection_density
#         awareness_density_matrix[i, j] = awareness_density
#
# # 保存数据到 CSV 文件
# np.savetxt("831_infection_density_matrix.csv", infection_density_matrix, delimiter=",")
# np.savetxt("831_awareness_density_matrix.csv", awareness_density_matrix, delimiter=",")

# 从 CSV 文件加载数据
infection_density_matrix = np.loadtxt("831_infection_density_matrix.csv", delimiter=",")
awareness_density_matrix = np.loadtxt("831_awareness_density_matrix.csv", delimiter=",")

# 绘制热力图
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
cbar = plt.colorbar()
cbar.ax.set_title('$\\rho^{A}$', pad=10)  # 在色标上方添加标题
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda_{info}$')

plt.subplot(1, 2, 2)
plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
cbar = plt.colorbar()
cbar.ax.set_title('$\\rho^{I}$', pad=10)  # 在色标上方添加标题
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda_{info}$')

plt.tight_layout()
plt.show()


# 对数据应用高斯平滑
plt.figure(figsize=(10, 6))
sigma = 1.0  # 高斯平滑的标准差，可以调整
# infection_density_matrix_smoothed = gaussian_filter(infection_density_matrix, sigma=sigma)
# awareness_density_matrix_smoothed = gaussian_filter(awareness_density_matrix, sigma=sigma)
# 平滑后的感知密度热力图
#plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.imshow(awareness_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
cbar = plt.colorbar()
cbar.ax.set_title('$\\rho^{A}$', pad=10)  # 在色标上方添加标题
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda$')

plt.tight_layout()
plt.savefig('实验4_感知λ和β热力图.pdf', format='pdf')
plt.show()


# 平滑后的感染密度热力图
plt.figure(figsize=(10, 6))

#plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.imshow(infection_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
cbar = plt.colorbar()
cbar.ax.set_title('$\\rho^{I}$', pad=10)  # 在色标上方添加标题
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda$')

plt.tight_layout()
plt.savefig('实验4_感染λ和β热力图.pdf', format='pdf')
plt.show()



