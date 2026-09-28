import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import itertools
from matplotlib.ticker import FuncFormatter

# 从 CSV 文件读取数据
df = pd.read_csv('830density_results.csv')

# 设置一个误差容忍值
tolerance = 1e-7
# 目标值范围
target_values = [round(i * 0.1, 1) for i in range(11)]  # 生成 [0, 0.1, ..., 1.0]
# 筛选 lambda_info 和 beta_U 都为 0.1 的整数倍的数据
filtered_data = df[(df['lambda_info'].isin(target_values)) & (df['beta_U'].isin(target_values))]
# 容差范围
tolerance = 1e-6

# 筛选 lambda_info 和 beta_U 接近目标值的数据
filtered_data = df[
    (np.abs(df['lambda_info'] - df['lambda_info'].round(1)) < tolerance) &
    (np.abs(df['beta_U'] - df['beta_U'].round(1)) < tolerance)
]
# 查看筛选后的数据
print(filtered_data)

# 计算 awareness_density 的平均值
awareness_mean = filtered_data['awareness_density'].mean()
infection_mean = filtered_data['infection_density'].mean()

print(f"awareness_density 和 infection_density 的平均值为: {awareness_mean},{infection_mean} ")

# 提取 lambda_info 和 lambda_star 的唯一值
lambda_info_values = np.unique(filtered_data['lambda_info'])
lambda_star_values = np.unique(filtered_data['beta_U'])

# 创建热力图矩阵
awareness_density_matrix = filtered_data.pivot(index='lambda_info', columns='beta_U', values='awareness_density').values
infection_density_matrix = filtered_data.pivot(index='lambda_info', columns='beta_U', values='infection_density').values


#对数据应用高斯平滑
plt.figure(figsize=(10, 6))

# 平滑后的感知密度热力图
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
plt.ylabel('$\\lambda_info$', fontsize=21)  # 增大y轴标签字体大小

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
plt.ylabel('$\\lambda_info$')
# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('25*25_mc感知lambda_info和β热力图.pdf', format='pdf')
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
plt.ylabel('$\\lambda_info$', fontsize=21)  # 增大y轴标签字体大小

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
plt.ylabel('$\\lambda_info$')
# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('25*25_mc感染lambda_info和β热力图.pdf', format='pdf')
plt.show()

# 计算感知密度的平均值，感染密度的平均值
average_awareness_density = np.mean(awareness_density_matrix)
average_infection_density = np.mean(infection_density_matrix)
# 输出平均值
print(f"感知密度的平均值: {average_awareness_density}")
print(f"感染密度的平均值: {average_infection_density}")

