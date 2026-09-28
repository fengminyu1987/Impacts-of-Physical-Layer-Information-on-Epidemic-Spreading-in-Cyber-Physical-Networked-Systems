import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import itertools
#
# # 参数设置
# num_nodes = 1000
# initial_infected_ratio = 0.01  # 初始感染节点比例
# delta = 0.8  # 信息遗忘率
# mu = 0.4  # 治愈率
# beta_A = 0.0  # 感知状态下对疾病免疫
# beta_U = 0.5  # 固定β_U值
# lambda_star = 0
#
# # 固定种子以保证每次生成相同的图和2-单纯形
# seed_value = 211
# random.seed(seed_value)
# # 生成ER图
# G_info = nx.erdos_renyi_graph(1000, p=6/995, seed=seed_value)
# # 2-单纯形概率
# prob_2_simplex = 4 / (999 * 998)
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
# # 输出构造的2-单纯形的数量
# print(f"Number of 2-simplices constructed: {len(simplices_2)}")
#
# # 初始化物理层网络
# G_epidemic = nx.watts_strogatz_graph(1000, 4, 0.5, seed=2)
# b_matrix = nx.to_numpy_array(G_epidemic)
#
# def get_neighbors(G, node):
#     return list(G.neighbors(node))
#
# def get_r_i_2(i, node_simplex_neighbors, lambda_star):
#     r_i_2 = 1
#     for (j, k) in node_simplex_neighbors[i]:
#         P_j_A = 1 if states[j] in ['AI', 'AS'] else 0
#         P_k_A = 1 if states[k] in ['AI', 'AS'] else 0
#         c_ijk = 1
#         r_i_2 *= (1 - c_ijk * P_j_A * P_k_A * lambda_star)
#
#     return r_i_2
#
# def calculate_r_i_3(i, b_matrix, states, theta):
#     k_i = len(get_neighbors(G_epidemic, i))  # 节点 i 在物理层的邻居数
#     sum_bji_pj_ai = sum(b_matrix[j, i] * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i))  # \sum_{j}b_{ji}P_{j}^{AI}
#     if k_i > 0:  # 避免除以零
#         fraction = sum_bji_pj_ai / k_i
#     else:
#         fraction = 0
#     r_i_3 = 1 - theta * fraction
#     return r_i_3
#
# def simulate_step(states, lambda_info, beta_U, theta):
#     new_states = states.copy()
#     for i in range(num_nodes):
#         if states[i] == 'AI':  # AI状态下的节点
#             if np.random.rand() <= delta:
#                 new_states[i] = 'UI'
#                 if np.random.rand() <= mu:
#                     new_states[i] = 'US'
#                 else:
#                     new_states[i] = 'AI'
#             else:
#                 new_states[i] = 'AI'
#                 if np.random.rand() <= mu:
#                     new_states[i] = 'AS'
#                 else:
#                     new_states[i] = 'AI'
#
#         elif states[i] == 'US':  # US状态下的节点
#             r_i_1 = np.prod([1 - lambda_info * (states[j] == 'AI' or states[j] == 'AS') for j in get_neighbors(G_info, i)])
#             #r_i_2 = get_r_i_2(i, node_simplex_neighbors, lambda_star)
#             r_i_3 = calculate_r_i_3(i, b_matrix, states, theta)
#             r_i = r_i_1 * r_i_3  #* r_i_2
#             if np.random.rand() <= 1 - r_i:
#                 new_states[i] = 'AS'
#                 QA_i = np.prod([1 - beta_A * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
#                 if np.random.rand() <= 1 - QA_i:
#                     new_states[i] = 'AI'
#                 else:
#                     new_states[i] = 'AS'
#             else:
#                 new_states[i] = 'US'
#                 QU_i = np.prod([1 - beta_U * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
#                 if np.random.rand() <= 1 - QU_i:
#                     new_states[i] = 'AI'
#                 else:
#                     new_states[i] = 'US'
#
#         elif states[i] == 'AS':  # AS状态下的节点
#             if np.random.rand() <= delta:
#                 new_states[i] = 'US'
#                 QU_i = np.prod([1 - beta_U * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
#                 if np.random.rand() <= 1 - QU_i:
#                     new_states[i] = 'AI'
#                 else:
#                     new_states[i] = 'US'
#             else:
#                 new_states[i] = 'AS'
#                 QA_i = np.prod([1 - beta_A * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
#                 if np.random.rand() <= 1 - QA_i:
#                     new_states[i] = 'AI'
#                 else:
#                     new_states[i] = 'AS'
#
#     return new_states
#
# # 设置参数范围
# lambda_info_values = np.arange(0, 1.1, 0.02) #左避右开
# theta_values = np.arange(0, 1.1, 0.02)
#
# # 存储结果
# awareness_density_matrix = np.zeros((len(lambda_info_values), len(theta_values)))
# infection_density_matrix = np.zeros((len(lambda_info_values), len(theta_values)))
#
# # 主循环
# max_iterations = 10000
# num_simulations = 20
#
# for i, lambda_info in enumerate(lambda_info_values):
#     print('lambda_info', lambda_info)
#     for j, theta in enumerate(theta_values):
#         print('theta', theta)
#         awareness_density_list = []
#         infection_density_list = []
#
#         # ###重复次数
#         for _ in range(num_simulations):
#             states = np.array(['US'] * num_nodes)
#             initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
#             states[initial_infected] = 'AI'
#
#             iterations = 0
#             while iterations < max_iterations:
#                 new_states = simulate_step(states, lambda_info, beta_U, theta)
#                 ρ_Sta_I_ratio = np.mean(np.isin(states, ['AI']))
#                 ρ_Nsta_I_ratio = np.mean(np.isin(new_states, ['AI']))
#                 ρ_Sta_A_ratio = np.mean(np.isin(states, ['AS', 'AI']))
#                 ρ_Nsta_A_ratio = np.mean(np.isin(new_states, ['AS', 'AI']))
#
#                 if np.max(np.abs(ρ_Sta_I_ratio - ρ_Nsta_I_ratio)) < 1e-6 and np.max(np.abs(ρ_Nsta_A_ratio - ρ_Sta_A_ratio)) < 1e-6:
#                     awareness_density_list.append(ρ_Nsta_A_ratio)
#                     infection_density_list.append(ρ_Nsta_I_ratio)
#                     break
#
#                 states = new_states
#                 iterations += 1
#
#             if iterations >= max_iterations:
#                 awareness_density_list.append(ρ_Nsta_A_ratio)
#                 infection_density_list.append(ρ_Nsta_I_ratio)
#
#         awareness_density_matrix[i, j] = np.mean(awareness_density_list)
#         infection_density_matrix[i, j] = np.mean(infection_density_list)
#
# # 保存数据到 CSV 文件
# data = {
#     'lambda_info': np.repeat(lambda_info_values, len(theta_values)),
#     'theta': np.tile(theta_values, len(lambda_info_values)),
#     'awareness_density': awareness_density_matrix.flatten(),
#     'infection_density': infection_density_matrix.flatten()
# }
# df = pd.DataFrame(data)
# df.to_csv('副本density_results.csv', index=False)
#
# print("数据已保存到 '副本density_results.csv'")

# 从 CSV 文件读取数据
df = pd.read_csv('副本density_results.csv')

# 提取 lambda_info 和 theta 的唯一值
lambda_info_values = np.unique(df['lambda_info'])
theta_values = np.unique(df['theta'])

# 创建热力图矩阵
awareness_density_matrix_fb = df.pivot(index='lambda_info', columns='theta', values='awareness_density').values
infection_density_matrix_fb = df.pivot(index='lambda_info', columns='theta', values='infection_density').values
#绘制热力图
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.imshow(awareness_density_matrix_fb, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('β=0.5_Awareness Density Heatmap')
plt.xlabel('$\\theta$')
plt.ylabel('$\\lambda_{info}$')

plt.subplot(1, 2, 2)
plt.imshow(infection_density_matrix_fb, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('β=0.5_Infection Density Heatmap')
plt.xlabel('$\\theta$')
plt.ylabel('$\\lambda_{info}$')

plt.tight_layout()
plt.show()

# 对数据应用高斯平滑
plt.figure(figsize=(14, 6))
sigma = 1.0  # 高斯平滑的标准差，可以调整
# infection_density_matrix_fb_smoothed = gaussian_filter(infection_density_matrix_fb, sigma=sigma)
# awareness_density_matrix_fb_smoothed = gaussian_filter(awareness_density_matrix_fb, sigma=sigma)
# 平滑后的感知密度热力图
plt.subplot(1, 2, 1)
#plt.imshow(awareness_density_matrix_fb, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.imshow(awareness_density_matrix_fb, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
plt.colorbar()
plt.title('β=0.5_Awareness Density Heatmap (Smoothed)')
plt.xlabel('$\\theta$')
plt.ylabel('$\\lambda$')

# 平滑后的感染密度热力图
plt.subplot(1, 2, 2)
#plt.imshow(infection_density_matrix_fb, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.imshow(infection_density_matrix_fb, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
plt.colorbar()
plt.title('β=0.5_Infection Density Heatmap (Smoothed)')
plt.xlabel('$\\theta$')
plt.ylabel('$\\lambda$')

plt.tight_layout()
plt.show()

# 绘制热力图
plt.figure(figsize=(14, 6))

# 感知节点密度热力图
plt.subplot(1, 2, 1)
plt.imshow(awareness_density_matrix_fb, cmap='YlGnBu', interpolation='nearest', aspect='auto')
plt.colorbar(label='Awareness Density')
plt.xticks(ticks=np.arange(len(theta_values)), labels=np.round(theta_values, 1))
plt.yticks(ticks=np.arange(len(lambda_info_values)), labels=np.round(lambda_info_values, 1))
plt.xlabel('Theta')
plt.ylabel('Lambda Info')
plt.title('Awareness Density Heatmap')

# 感染节点密度热力图
plt.subplot(1, 2, 2)
plt.imshow(infection_density_matrix_fb, cmap='YlOrRd', interpolation='nearest', aspect='auto')
plt.colorbar(label='Infection Density')
plt.xticks(ticks=np.arange(len(theta_values)), labels=np.round(theta_values, 1))
plt.yticks(ticks=np.arange(len(lambda_info_values)), labels=np.round(lambda_info_values, 1))
plt.xlabel('Theta')
plt.ylabel('Lambda Info')
plt.title('Infection Density Heatmap')

plt.tight_layout()
plt.show()