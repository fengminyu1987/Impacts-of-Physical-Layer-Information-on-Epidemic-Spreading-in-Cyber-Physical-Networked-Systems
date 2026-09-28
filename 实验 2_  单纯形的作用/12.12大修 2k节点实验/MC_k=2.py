import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import powerlaw
import pandas as pd
import itertools

# # 参数设置
# num_nodes = 2000
# initial_infected_ratio = 0.01  # 初始感染节点比例
# lambda_info = 0.5  # 信息传播率
# lambda_star = 0.5  # 单纯形传播率
# theta = 0.5  # 物理层传播率
# alpha = 10   #反应强度
#
# delta = 0.8  # 信息遗忘率
#
# mu = 0.4  # 治愈率
# beta_A = 0.0  # 感知状态下对疾病免疫
#
# # 固定种子以保证每次生成相同的图和2-单纯形
# seed_value = 211
# random.seed(seed_value)
# # 生成ER图
# G_info = nx.erdos_renyi_graph(2000, p=6/995, seed=seed_value)
# # 2-单纯形概率
# prob_2_simplex = 1 * 4 / (1999 * 1998) # k=2
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
# G_epidemic = nx.watts_strogatz_graph(2000, 4, 0.5, seed=2)
# b_matrix = nx.to_numpy_array(G_epidemic)
# # 初始化节点状态
# states = np.array(['US'] * num_nodes)  # 所有节点初始状态为US
# initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
# states[initial_infected] = 'AI'  # 初始感染节点
#
# # 找信息和物理层邻居
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
#     r_i_3 = 1 - 1 / (1 + np.exp(-alpha * (fraction-theta)))#r_i_3 = 1 - theta * fraction #np.exp(-theta * fraction)
#     return r_i_3
#
# def simulate_step(states, beta_U):
#     new_states = states.copy()
#     for i in range(num_nodes):
#         if states[i] == 'AI':  # AI状态下的节点
#             #print(f"Node {i} AI -> ", end="")
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
#             #print(f"{new_states[i]}")
#
#         elif states[i] == 'US':  # US状态下的节点
#             #print(f"Node {i} US -> ", end="")
#             #lambda_star = 0.8 * lambda_info
#             #r_i_1 = np.prod([1 - lambda_info * (states[j] == 'AI' or states[j] == 'AS') for j in get_neighbors(G_info, i)])
#             r_i_2 = get_r_i_2(i, node_simplex_neighbors, lambda_star)
#             #r_i_3 = calculate_r_i_3(i, b_matrix, states, theta)
#             #r_i = r_i_1 * r_i_3 * r_i_2
#             r_i = r_i_2
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
#             #print(f"{new_states[i]}")
#
#         elif states[i] == 'AS':  # AS状态下的节点
#             #print(f"Node {i} AS -> ", end="")
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
#             #print(f"{new_states[i]}")
#
#     return new_states
#
#     #### 主函数入口部分
# max_iterations = 10000  # 最大迭代次数
# beta_U_values = np.arange(0, 1.02, 0.02)  # β_U 的取值范围，左闭右开区间
# ρ_A = []
# ρ_I = []
# num_simulations = 100  # 仿真次数
# for beta_U in beta_U_values:
#     print("beta_U", (beta_U/1))
#     for i in range(5):
#         print('xxxxxxxxxx')
#     awareness_density_list = []  # 存储每次仿真的感知节点密度
#     infection_density_list = []  # 存储每次仿真的感染节点密度
#     # 进行多次仿真
#     for _ in range(num_simulations):
#         states = np.array(['US'] * num_nodes)
#         initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
#         states[initial_infected] = 'AI'
#
#         iterations = 0
#         while iterations < max_iterations:
#             #simulate_step()得到每个beta_u下 所有节点状态
#             new_states = simulate_step(states, beta_U)
#             ρ_Sta_I_ratio = np.mean(np.isin(states, ['AI']))
#             ρ_Nsta_I_ratio = np.mean(np.isin(new_states, ['AI']))
#             ρ_Sta_A_ratio = np.mean(np.isin(states, ['AS', 'AI']))
#             ρ_Nsta_A_ratio = np.mean(np.isin(new_states, ['AS', 'AI']))
#
#             if np.max(np.abs(ρ_Sta_I_ratio - ρ_Nsta_I_ratio)) < 1e-8 and np.max(np.abs(ρ_Nsta_A_ratio - ρ_Sta_A_ratio)) < 1e-8:
#                 awareness_density_list.append(ρ_Nsta_A_ratio)
#                 infection_density_list.append(ρ_Nsta_I_ratio)
#                 break
#
#             states = new_states
#             iterations += 1
#
#         # 如果循环在未满足稳态条件下结束，将最后一次的密度值添加到列表中
#         if iterations >= max_iterations:
#             awareness_density_list.append(ρ_Nsta_A_ratio)
#             infection_density_list.append(ρ_Nsta_I_ratio)
#
#     ρ_A.append(np.mean(awareness_density_list))  # 计算感知节点密度的平均值
#     ρ_I.append(np.mean(infection_density_list))  # 计算感染节点密度的平均值
#
# # 保存数据到 CSV 文件
# data = {
#     'beta_U': beta_U_values,
#     'infection_density': ρ_I,
#     'awareness_density': ρ_A
# }
# df = pd.DataFrame(data)
# df.to_csv('MC_k=2_加进度条版822.csv', index=False)
#
# print(f"稳态时处于感知状态的节点比例：{ρ_A}")
# print(f"稳态时处于感染状态的节点比例：{ρ_I}")

# 读取实验数据
experiment_df = pd.read_csv('MC_k=2_加进度条版822.csv')

# 提取数据
beta_U_exp = experiment_df['beta_U']
rho_I_exp = experiment_df['infection_density']
rho_A_exp = experiment_df['awareness_density']

# 可视化结果
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(beta_U_exp,rho_A_exp, marker='o')
plt.title('Aware Nodes Ratio with β_U')
plt.xlabel('β_U')
plt.ylabel('Aware Nodes Ratio')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(beta_U_exp, rho_I_exp, marker='o')
plt.title('Infected Nodes Ratio with β_U')
plt.xlabel('β_U')
plt.ylabel('Infected Nodes Ratio')
plt.grid(True)

plt.tight_layout()
plt.show()