import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import itertools
from matplotlib.ticker import FuncFormatter

# 参数设置
num_nodes = 1000
initial_infected_ratio = 0.01  # 初始感染节点比例
delta = 0.8  # 信息遗忘率
mu = 0.4  # 治愈率
beta_A = 0.0  # 感知状态下对疾病免疫
#beta_U = 0.5  # 固定β_U值
lambda_info = 0  # 固定lambda_info值
lambda_star = 0
theta = None  # 固定theta值
alpha = 10

# 固定种子以保证每次生成相同的图和2-单纯形
seed_value = 211
random.seed(seed_value)
# 生成ER图
G_info = nx.erdos_renyi_graph(1000, p=6/995, seed=seed_value)
# 2-单纯形概率
prob_2_simplex = 4 / (999 * 998)
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

# 输出构造的2-单纯形的数量
print(f"Number of 2-simplices constructed: {len(simplices_2)}")

# 初始化物理层网络
G_epidemic = nx.watts_strogatz_graph(1000, 4, 0.5, seed=2)
b_matrix = nx.to_numpy_array(G_epidemic)

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
    k_i = len(get_neighbors(G_epidemic, i))  # 节点 i 在物理层的邻居数
    sum_bji_pj_ai = sum(b_matrix[j, i] * (states[j] == 'AI') for j in get_neighbors(G_epidemic, i))  # \sum_{j}b_{ji}P_{j}^{AI}
    if k_i > 0:  # 避免除以零
        fraction = sum_bji_pj_ai / k_i
    else:
        fraction = 0
    r_i_3 = 1 - 1 / (1 + np.exp(-alpha * (fraction - theta)))  # np.exp(-theta * proportion)
    return r_i_3

def simulate_step(states, lambda_star, beta_U, theta):
    new_states = states.copy()
    for i in range(num_nodes):
        if states[i] == 'AI':  # AI状态下的节点
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

        elif states[i] == 'US':  # US状态下的节点
            #r_i_1 = np.prod([1 - lambda_info * (states[j] == 'AI' or states[j] == 'AS') for j in get_neighbors(G_info, i)])
            #r_i_2 = get_r_i_2(i, node_simplex_neighbors, lambda_star)
            r_i_3 = calculate_r_i_3(i, b_matrix, states, theta)
            r_i = r_i_3
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

        elif states[i] == 'AS':  # AS状态下的节点
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

# 设置参数范围
theta_values = np.linspace(0, 1, 26)
beta_values = np.linspace(0, 1, 26)

# 存储结果
# awareness_density_matrix = np.zeros((len(beta_values), len(theta_values)))
# infection_density_matrix = np.zeros((len(beta_values), len(theta_values)))

awareness_density_matrix = np.zeros((len(theta_values), len(beta_values)))
infection_density_matrix = np.zeros((len(theta_values), len(beta_values)))

# 主循环
max_iterations = 10000
#num_simulations = 50
num_simulations = 10  #11/12修改

for i, theta in enumerate(theta_values):
    for j, beta_U in enumerate(beta_values):
        print('theta and beta', theta, beta_U)
        awareness_density_list = []
        infection_density_list = []

        # 进行多次仿真
        for _ in range(num_simulations):
            states = np.array(['US'] * num_nodes)
            initial_infected = np.random.choice(num_nodes, int(num_nodes * initial_infected_ratio), replace=False)
            states[initial_infected] = 'AI'

            iterations = 0
            while iterations < max_iterations:
                new_states = simulate_step(states, lambda_star, beta_U, theta)
                ρ_Sta_I_ratio = np.mean(np.isin(states, ['AI']))
                ρ_Nsta_I_ratio = np.mean(np.isin(new_states, ['AI']))
                ρ_Sta_A_ratio = np.mean(np.isin(states, ['AS', 'AI']))
                ρ_Nsta_A_ratio = np.mean(np.isin(new_states, ['AS', 'AI']))

                if np.max(np.abs(ρ_Sta_I_ratio - ρ_Nsta_I_ratio)) < 1e-6 and np.max(np.abs(ρ_Nsta_A_ratio - ρ_Sta_A_ratio)) < 1e-6:
                    awareness_density_list.append(ρ_Nsta_A_ratio)
                    infection_density_list.append(ρ_Nsta_I_ratio)
                    break
                states = new_states
                iterations += 1

            if iterations >= max_iterations:
                awareness_density_list.append(ρ_Nsta_A_ratio)
                infection_density_list.append(ρ_Nsta_I_ratio)

        # 计算平均值并存储
        awareness_density_matrix[i, j] = np.mean(awareness_density_list)
        infection_density_matrix[i, j] = np.mean(infection_density_list)

# 保存数据到 CSV 文件
data = {
    'theta': np.repeat(theta_values, len(beta_values)),
    'beta_U': np.tile(beta_values, len(theta_values)),
    'awareness_density': awareness_density_matrix.flatten(),
    'infection_density': infection_density_matrix.flatten(),
}

df = pd.DataFrame(data)
df.to_csv('2MC_theta和beta_density.csv', index=False)

print("2MC_theta和beta_density.csv")

# 从 CSV 文件读取数据
df = pd.read_csv('2MC_theta和beta_density.csv')

# 提取 lambda_info 和 lambda_star 的唯一值
theta_values = np.unique(df['theta'])
lambda_star_values = np.unique(df['beta_U'])

# 创建热力图矩阵
awareness_density_matrix = df.pivot(index='theta', columns='beta_U', values='awareness_density').values
infection_density_matrix = df.pivot(index='theta', columns='beta_U', values='infection_density').values

# 自定义截断函数，只保留前4位数
def truncate_values(matrix, decimal_places=3):
    factor = 10 ** decimal_places  # 用于控制截断的位数
    return np.floor(matrix * factor) / factor  # 乘以10的4次方，然后用floor去掉后面的位数

# 对感知密度和感染密度矩阵进行截断处理，只保留前 4 位数
awareness_density_matrix = truncate_values(awareness_density_matrix, 3)
infection_density_matrix = truncate_values(infection_density_matrix, 3)

#绘制热力图
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('831_Awareness Density Heatmap')
plt.xlabel('$\\beta$')
plt.ylabel('$\\theta$')

plt.subplot(1, 2, 2)
plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('831_Infection Density Heatmap')
plt.xlabel('$\\beta$')
plt.ylabel('$\\theta$')
plt.tight_layout()
plt.show()

# # 对数据应用高斯平滑
# plt.figure(figsize=(14, 6))
# plt.subplot(1, 2, 1)
# plt.imshow(awareness_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
# plt.colorbar()
# plt.title('831_Awareness Density Heatmap (Smoothed)')
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\theta$')
#
# # 平滑后的感染密度热力图
# plt.subplot(1, 2, 2)
# plt.imshow(infection_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
# plt.colorbar()
# plt.title('831_Infection Density Heatmap (Smoothed)')
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\theta$')
#
# plt.tight_layout()
# plt.show()


# 对数据应用高斯平滑
plt.figure(figsize=(10, 6))
sigma = 1.0  # 高斯平滑的标准差，可以调整
# 平滑后的感知密度热力图
#plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.imshow(awareness_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')

# 自定义格式化函数，将 0.0 显示为 0
def custom_formatter(x, pos):
    if x == 0:
        return '0'
    else:
        return '{:.1f}'.format(x)
# 使用自定义的格式化函数来格式化刻度标签
ax = plt.gca()
ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))
ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))

# 添加标题和标签
plt.xlabel('$\\beta$', fontsize=21)  # 增大x轴标签字体大小
plt.ylabel('$\\theta$', fontsize=21)  # 增大y轴标签字体大小

# 设置刻度字体大小
plt.xticks(fontsize=19)  # 增大x轴刻度字体大小
plt.yticks(fontsize=19)  # 增大y轴刻度字体大小

cbar = plt.colorbar()
# 设置颜色条刻度字体大小为19
cbar.ax.tick_params(labelsize=19)
# 获取颜色条的最小值和最大值
vmin = cbar.vmin
vmax = cbar.vmax

# 设置颜色条的刻度为每隔0.2一个刻度，并使用 vmax 作为结束值
cbar.set_ticks(np.arange(vmin, vmax+0.01 , 0.2))  # +0.2 确保包含 vmax

cbar.ax.set_title('$\\rho^{A}$', pad=10, fontsize=21)  # 在色标上方添加标题
plt.xlabel('$\\beta$')
plt.ylabel('$\\theta$')
# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('实验4_mc感知theta和β热力图.pdf', format='pdf')
plt.show()


# 平滑后的感染密度热力图
plt.figure(figsize=(10, 6))
#plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.imshow(infection_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
# 自定义格式化函数，将 0.0 显示为 0
def custom_formatter(x, pos):
    if x == 0:
        return '0'
    else:
        return '{:.1f}'.format(x)
# 使用自定义的格式化函数来格式化刻度标签
ax = plt.gca()
ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))
ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))

# 添加标题和标签
plt.xlabel('$\\beta$', fontsize=21)  # 增大x轴标签字体大小
plt.ylabel('$\\theta$', fontsize=21)  # 增大y轴标签字体大小

# 设置刻度字体大小
plt.xticks(fontsize=19)  # 增大x轴刻度字体大小
plt.yticks(fontsize=19)  # 增大y轴刻度字体大小

cbar = plt.colorbar()
# 设置颜色条刻度字体大小为19
cbar.ax.tick_params(labelsize=19)
# # 获取颜色条的最小值和最大值
vmin = cbar.vmin
vmax = cbar.vmax

# 设置颜色条的刻度为每隔0.2一个刻度，并使用 vmax 作为结束值
cbar.set_ticks(np.arange(vmin, vmax+0.01 , 0.2))  # +0.2 确保包含 vmax

cbar.ax.set_title('$\\rho^{I}$', pad=10, fontsize=21)  # 在色标上方添加标题
plt.xlabel('$\\beta$')
plt.ylabel('$\\theta$')
# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('实验4_mc感染theta和β热力图.pdf', format='pdf')
plt.show()

# 计算感知密度的平均值
average_awareness_density = np.mean(awareness_density_matrix)

# 计算感染密度的平均值
average_infection_density = np.mean(infection_density_matrix)

# 输出平均值
print(f"感知密度的平均值: {average_awareness_density}")
print(f"感染密度的平均值: {average_infection_density}")







