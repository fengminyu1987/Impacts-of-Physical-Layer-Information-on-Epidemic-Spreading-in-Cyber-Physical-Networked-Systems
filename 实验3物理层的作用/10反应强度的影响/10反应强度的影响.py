import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import powerlaw
import pandas as pd
import itertools

# 参数设置
initial_infected_ratio = 0.01
num_nodes = 1000

#信息层参数
lambda_info = 0
lambda_star = 0  # ###只考虑物理层信息的影响，加上信息层，物理层作用太小
alpha = 10
# 遍历theta值求密度
delta = 0.8

#物理层参数
mu = 0.4
beta_A = 0.0  # 感知状态下对疾病免疫

# 固定种子以保证每次生成相同的图和2-单纯形
seed_value = 211
random.seed(seed_value)

# 生成ER图
G_info = nx.erdos_renyi_graph(1000, p=6/995, seed=seed_value)

# 2-单纯形概率
prob_2_simplex = 1 * 4 / (999 * 998)

# 用于保存构造的2-单纯形
simplices_2 = []

# 用于保存每个节点的2-单纯形邻居
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

a_matrix = nx.to_numpy_array(G_info)

# 生成2.5物理层
G_epidemic = nx.watts_strogatz_graph(1000, 4, 0.5, seed=2)
b_matrix = nx.to_numpy_array(G_epidemic)

# 找信息和物理层邻居的函数
def get_neighbors(G, node):
    return list(G.neighbors(node))

# 计算r_i_1的函数
def get_r_i_1(a_matrix, P_A):
     return np.prod(1 - a_matrix * P_A[:, None] * lambda_info, axis=0)

def get_r_i_2(node_simplex_neighbors, P_A, lambda_star):
    num_nodes = len(P_A)
    r_i_2 = np.ones(num_nodes)
    for i in range(num_nodes):
        product = 1
        for (j, k) in node_simplex_neighbors[i]:
            c_ijk = P_A[j] * P_A[k]
            product *= (1 - c_ijk * lambda_star)
        r_i_2[i] = product
    return r_i_2

def get_r_i_3(b_matrix, P_AI, theta, alpha):
    num_nodes = b_matrix.shape[0]
    r_i_3 = np.ones(num_nodes)
    for i in range(num_nodes):
        k_i = np.sum(b_matrix[i])
        sum_bji_Pj = np.sum(b_matrix[i] * P_AI)
        fraction = sum_bji_Pj / k_i if k_i > 0 else 0
        r_i_3[i] = 1 - 1 / (1 + np.exp(-alpha * (fraction-theta)))
    return r_i_3

def get_q_i(b_matrix, P_AI, beta):
    return np.prod(1 - b_matrix * P_AI[:, None] * beta, axis=0)

# 迭代更新节点状态概率的函数
def iterate_probabilities(beta_U, theta, alpha):
    P_AI = np.zeros(num_nodes)
    P_AS = np.zeros(num_nodes)
    P_US = np.ones(num_nodes)
    initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
    P_AI[initial_infected] = 1
    P_US[initial_infected] = 0

    max_iterations = 10000
    tolerance = 1e-6

    for iteration in range(max_iterations):
        P_A = P_AI + P_AS
        r_i = get_r_i_1(a_matrix, P_A) * get_r_i_2(node_simplex_neighbors, P_A, lambda_star) * get_r_i_3(b_matrix, P_AI, theta, alpha)
        q_i_A = get_q_i(b_matrix, P_AI, beta_A)
        q_i_U = get_q_i(b_matrix, P_AI, beta_U)

        P_US_next = P_AI * delta * mu + P_US * r_i * q_i_U + P_AS * delta * q_i_U
        P_AS_next = P_AI * (1 - delta) * mu + P_US * (1 - r_i) * q_i_A + P_AS * (1 - delta) * q_i_A
        P_AI_next = P_AI * (1 - mu) + P_US * ((1 - r_i) * (1 - q_i_A) + r_i * (1 - q_i_U)) + P_AS * (
                    delta * (1 - q_i_U) + (1 - delta) * (1 - q_i_A))

        if np.max(np.abs(P_US_next - P_US)) < tolerance and np.max(np.abs(P_AS_next - P_AS)) < tolerance and np.max(
                np.abs(P_AI_next - P_AI)) < tolerance:
            break
        P_US, P_AS, P_AI = P_US_next, P_AS_next, P_AI_next

    infection_density = np.mean(P_AI)
    awareness_density = np.mean(P_A)
    return infection_density, awareness_density


# 主函数，遍历 beta 和 theta 的值，得到感染密度和感知密度
theta_values = [0.3, 0.5, 0.7]
beta_U_values = np.arange(0, 1.02, 0.02)
results = []

for theta in theta_values:
    print('theta', theta)
    infection_densities = []
    awareness_densities = []
    for beta_U in beta_U_values:
        infection_density, awareness_density = iterate_probabilities(beta_U, theta, alpha)
        infection_densities.append(infection_density)
        awareness_densities.append(awareness_density)
    # 将结果添加到 DataFrame 中
    df = pd.DataFrame({
        'beta_U': beta_U_values,
        'infection_density': infection_densities,
        'awareness_density': awareness_densities
    })
    df['theta'] = theta

    # 保存为 CSV 文件
    df.to_csv(f'results_theta_{theta}.csv', index=False)
#

# 读取 CSV 文件并绘制图形
theta_values = [0.3, 0.5, 0.7]

# 绘制感染密度曲线
plt.figure(figsize=(10, 6))
for theta in theta_values:
    df = pd.read_csv(f'results_theta_{theta}.csv')
    plt.plot(df['beta_U'], df['infection_density'], label=f'θ={theta}')
plt.xlabel('beta_U')
plt.ylabel('Infection Density')
plt.xlim(0,1)
plt.title('Infection Density vs. beta_U for Different θ')
plt.legend()
plt.grid(True)
plt.show()

# 绘制感知密度曲线
plt.figure(figsize=(10, 6))
for theta in theta_values:
    df = pd.read_csv(f'results_theta_{theta}.csv')
    plt.plot(df['beta_U'], df['awareness_density'], label=f'θ={theta}')
plt.xlabel('beta_U')
plt.ylabel('Awareness Density')
plt.xlim(0, 1)
plt.ylim(0,)
plt.title('Awareness Density vs. beta_U for Different θ')
plt.legend()
plt.grid(True)
plt.show()