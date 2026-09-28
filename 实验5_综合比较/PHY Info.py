import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import itertools

# 参数设置
num_nodes = 1000
initial_infected_ratio = 0.01
lambda_info = 0   ##不考虑信息层，其对物理层信息影响太大
lambda_star = 0
alpha = 10
delta = 0.8

mu = 0.4
beta_A = 0.0

# 固定种子以保证每次生成相同的图和2-单纯形
seed_value = 211
random.seed(seed_value)

# 生成ER图
G_info = nx.erdos_renyi_graph(1000, p=6/995, seed=seed_value)

# 2-单纯形概率
prob_2_simplex = 4 / (999 * 998)

# 用于保存构造的2-单纯形
simplices_2 = []
node_simplex_neighbors = {node: [] for node in G_info.nodes}

# 遍历所有的三元节点组合(i, j, k)
nodes = list(G_info.nodes)
for i, j, k in itertools.combinations(nodes, 3):
    if random.random() < prob_2_simplex:
        if not G_info.has_edge(i, j):
            G_info.add_edge(i, j)
        if not G_info.has_edge(i, k):
            G_info.add_edge(i, k)
        if not G_info.has_edge(j, k):
            G_info.add_edge(j, k)
        simplices_2.append((i, j, k))
        node_simplex_neighbors[i].append((j, k))
        node_simplex_neighbors[j].append((i, k))
        node_simplex_neighbors[k].append((i, j))

print(f"Number of 2-simplices constructed: {len(simplices_2)}")

# 初始化物理层网络
G_epidemic = nx.watts_strogatz_graph(1000, 4, 0.5, seed=2)
b_matrix = nx.to_numpy_array(G_epidemic)
states = np.array(['US'] * num_nodes)
initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
states[initial_infected] = 'AI'

def get_neighbors(G, node):
    return list(G.neighbors(node))

def get_r_i_2(i, node_simplex_neighbors, lambda_star):
    r_i_2 = 1
    for (j, k) in node_simplex_neighbors[i]:
        P_j_A = 1 if states[j] in ['AI', 'AS'] else 0
        P_k_A = 1 if states[k] in ['AI', 'AS'] else 0
        c_ijk = 1
        r_i_2 *= (1 - c_ijk * P_j_A * P_k_A * lambda_star)

    return r_i_2

def calculate_r_i_3(i, b_matrix, states, theta):
    k_i = len(get_neighbors(G_epidemic, i))
    sum_bji_pj_ai = sum(b_matrix[j, i] * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i))
    fraction = sum_bji_pj_ai / k_i if k_i > 0 else 0
    r_i_3 = 1 - 1 / (1 + np.exp(-alpha * (fraction-theta)))
    return r_i_3

def simulate_step(states, beta_U, theta):
    new_states = states.copy()
    for i in range(num_nodes):
        if states[i] == 'AI':
            if np.random.rand() <= delta:
                new_states[i] = 'UI'
                if np.random.rand() <= mu:
                    new_states[i] = 'US'
                else:
                    new_states[i] = 'AI'
            else:
                new_states[i] = 'AI'
                if np.random.rand() <= mu:
                    new_states[i] = 'AS'
                else:
                    new_states[i] = 'AI'
        elif states[i] == 'US':
            r_i_1 = np.prod([1 - lambda_info * (states[j] in ['AI', 'AS']) for j in get_neighbors(G_info, i)])
            r_i_2 = get_r_i_2(i, node_simplex_neighbors, lambda_star)
            r_i_3 = calculate_r_i_3(i, b_matrix, states, theta)
            r_i = r_i_3  # * r_i_2 * r_i_1
            if np.random.rand() <= 1 - r_i:
                new_states[i] = 'AS'
                QA_i = np.prod([1 - beta_A * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
                if np.random.rand() <= 1 - QA_i:
                    new_states[i] = 'AI'
                else:
                    new_states[i] = 'AS'
            else:
                new_states[i] = 'US'
                QU_i = np.prod([1 - beta_U * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
                if np.random.rand() <= 1 - QU_i:
                    new_states[i] = 'AI'
                else:
                    new_states[i] = 'US'
        elif states[i] == 'AS':
            if np.random.rand() <= delta:
                new_states[i] = 'US'
                QU_i = np.prod([1 - beta_U * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
                if np.random.rand() <= 1 - QU_i:
                    new_states[i] = 'AI'
                else:
                    new_states[i] = 'US'
            else:
                new_states[i] = 'AS'
                QA_i = np.prod([1 - beta_A * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i)])
                if np.random.rand() <= 1 - QA_i:
                    new_states[i] = 'AI'
                else:
                    new_states[i] = 'AS'

    return new_states

# #####主循环：针对不同的 theta 值
thetas = [0.76]
max_iterations = 20000
beta_U_values = np.arange(0, 1.02, 0.02)
num_simulations = 100

ρ_A_dict = {theta: [] for theta in thetas}
ρ_I_dict = {theta: [] for theta in thetas}

for theta in thetas:
    print(f"Running simulations for theta = {theta}")
    for beta_U in beta_U_values:
        print('beta_U', beta_U)
        awareness_density_list = []
        infection_density_list = []
        for _ in range(num_simulations):
            states = np.array(['US'] * num_nodes)
            initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
            states[initial_infected] = 'AI'
            iterations = 0
            while iterations < max_iterations:
                new_states = simulate_step(states, beta_U, theta)   #    ##主代码
                ρ_Sta_I_ratio = np.mean(np.isin(states, ['AI']))
                ρ_Nsta_I_ratio = np.mean(np.isin(new_states, ['AI']))
                ρ_Sta_A_ratio = np.mean(np.isin(states, ['AS', 'AI']))
                ρ_Nsta_A_ratio = np.mean(np.isin(new_states, ['AS', 'AI']))

                if np.max(np.abs(ρ_Sta_I_ratio - ρ_Nsta_I_ratio)) < 1e-10 and np.max(np.abs(ρ_Nsta_A_ratio - ρ_Sta_A_ratio)) < 1e-10:
                    awareness_density_list.append(ρ_Nsta_A_ratio)
                    infection_density_list.append(ρ_Nsta_I_ratio)
                    break

                states = new_states
                iterations += 1

            if iterations >= max_iterations:
                awareness_density_list.append(ρ_Nsta_A_ratio)
                infection_density_list.append(ρ_Nsta_I_ratio)

        ρ_A_dict[theta].append(np.mean(awareness_density_list))
        print('ρa和ρi', ρ_Nsta_A_ratio, ρ_Nsta_I_ratio)
        ρ_I_dict[theta].append(np.mean(infection_density_list))

# 保存数据到 CSV 文件
data = {
    'beta_U': beta_U_values,
    **{f'awareness_density_theta_{theta}': ρ_A_dict[theta] for theta in thetas},
    **{f'infection_density_theta_{theta}': ρ_I_dict[theta] for theta in thetas}
}
df = pd.DataFrame(data)
df.to_csv('实验5——phy info.csv', index=False)

# 读取实验数据
experiment_df = pd.read_csv('实验5——phy info.csv')
thetas = [0.76]
# 提取数据
beta_U_exp = experiment_df['beta_U']
ρ_A_exp = {theta: experiment_df[f'awareness_density_theta_{theta}'] for theta in thetas}
ρ_I_exp = {theta: experiment_df[f'infection_density_theta_{theta}'] for theta in thetas}

# 可视化结果

# 绘制感知密度
plt.figure(figsize=(10, 6))
plt.plot(beta_U_exp, ρ_A_exp[0.76], '^-.', label='$\\theta=0.76$')
# plt.plot(beta_U_exp, ρ_A_exp[0.5], 'o-', label='$\\theta=0.5$')
# plt.plot(beta_U_exp, ρ_A_exp[0.7], 's--', label='$\\theta=0.7$')
plt.xlim(0, 1)
plt.ylim(0, 0.9)
plt.xlabel('$\\beta$')
plt.ylabel('$\\rho^{A}$')
# plt.legend()
# 感知密度绘图部分的继续
plt.grid(True)

# 调整布局并显示图形
plt.tight_layout()
plt.savefig('实验5_感知密度PHY_Info.pdf', format='pdf')
plt.show()

# 绘制感染密度
plt.figure(figsize=(10, 6))
plt.plot(beta_U_exp, ρ_I_exp[0.76], '^-.', label='$\\theta=0.76$')
# plt.plot(beta_U_exp, ρ_I_exp[0.5], 'o-', label='$\\theta=0.5$')
# plt.plot(beta_U_exp, ρ_I_exp[0.7], 's--', label='$\\theta=0.7$')
plt.xlim(0, 1)
plt.ylim(0, 0.7)
plt.xlabel('$\\beta$')
plt.ylabel('$\\rho^{I}$')
plt.legend()
plt.grid(True)

# 调整布局并显示图形
plt.tight_layout()
plt.savefig('实验5_感染密度PHY_Info.pdf', format='pdf')
plt.show()

