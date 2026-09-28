import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import itertools
from matplotlib.ticker import FuncFormatter

# 从 CSV 文件读取数据
df = pd.read_csv('MC_λ_star和β_density.csv')

# 提取 lambda_star 和 lambda_star 的唯一值
lambda_star_values = np.unique(df['lambda_star'])
beta_values = np.unique(df['beta_U'])

# 创建热力图矩阵
awareness_density_matrix = df.pivot(index='lambda_star', columns='beta_U', values='awareness_density').values
infection_density_matrix = df.pivot(index='lambda_star', columns='beta_U', values='infection_density').values


# 设置筛选条件：lambda_star 和 beta_U 为 0.1 的整数倍
# 设置一个误差容忍值
tolerance = 1e-7
# 目标值范围
target_values = [round(i * 0.1, 1) for i in range(11)]  # 生成 [0, 0.1, ..., 1.0]
# 筛选 lambda_star 和 beta_U 都为 0.1 的整数倍的数据
filtered_data = df[(df['lambda_star'].isin(target_values)) & (df['beta_U'].isin(target_values))]
# 容差范围
tolerance = 1e-6

# 筛选 lambda_star 和 beta_U 接近目标值的数据
filtered_data = df[
    (np.abs(df['lambda_star'] - df['lambda_star'].round(1)) < tolerance) &
    (np.abs(df['beta_U'] - df['beta_U'].round(1)) < tolerance)
]
# 查看筛选后的数据
print(filtered_data)

# 计算 awareness_density 的平均值
awareness_mean = filtered_data['awareness_density'].mean()
infection_mean = filtered_data['infection_density'].mean()

print(f"奇数行数据，awareness_density 和 infection_density 的平均值为: {awareness_mean},{infection_mean} ")

# 提取 lambda_info 和 lambda_star 的唯一值
lambda_star_values = np.unique(filtered_data['lambda_star'])
lambda_star_values = np.unique(filtered_data['beta_U'])

# 创建热力图矩阵
awareness_density_matrix = filtered_data.pivot(index='lambda_star', columns='beta_U', values='awareness_density').values
infection_density_matrix = filtered_data.pivot(index='lambda_star', columns='beta_U', values='infection_density').values




# 自定义截断函数，只保留前4位数
def truncate_values(matrix, decimal_places=2):
    factor = 10 ** decimal_places  # 用于控制截断的位数
    return np.floor(matrix * factor) / factor  # 乘以10的4次方，然后用floor去掉后面的位数

# 对感知密度和感染密度矩阵进行截断处理，只保留前 4 位数
awareness_density_matrix = truncate_values(awareness_density_matrix, 2)
infection_density_matrix = truncate_values(infection_density_matrix, 2)

#绘制热力图
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('831_Awareness Density Heatmap')
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda^{*}$')

plt.subplot(1, 2, 2)
plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('831_Infection Density Heatmap')
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda^{*}$')
plt.tight_layout()
plt.show()

# # 对数据应用高斯平滑
# plt.figure(figsize=(14, 6))
# plt.subplot(1, 2, 1)
# plt.imshow(awareness_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
# plt.colorbar()
# plt.title('831_Awareness Density Heatmap (Smoothed)')
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\lambda^{*}$')
#
# # 平滑后的感染密度热力图
# plt.subplot(1, 2, 2)
# plt.imshow(infection_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
# plt.colorbar()
# plt.title('831_Infection Density Heatmap (Smoothed)')
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\lambda^{*}$')
# plt.savefig('λ*和beta热力图.pdf', format='pdf')
#
# plt.tight_layout()
# plt.show()

# 对数据应用高斯平滑
plt.figure(figsize=(10, 6))
sigma = 1.0  # 高斯平滑的标准差，可以调整
# infection_density_matrix_smoothed = gaussian_filter(infection_density_matrix, sigma=sigma)
# awareness_density_matrix_smoothed = gaussian_filter(awareness_density_matrix, sigma=sigma)
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
plt.ylabel('$\\lambda^{*}$', fontsize=21)  # 增大y轴标签字体大小

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
plt.ylabel('$\\lambda^{*}$')
# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('实验4_mc感知λstar和β热力图.pdf', format='pdf')
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
plt.ylabel('$\\lambda^{*}$', fontsize=21)  # 增大y轴标签字体大小

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
plt.ylabel('$\\lambda^{*}$')
# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('实验4_mc感染λstar和β热力图.pdf', format='pdf')
plt.show()

# 计算感知密度的平均值
average_awareness_density = np.mean(awareness_density_matrix)

# 计算感染密度的平均值
average_infection_density = np.mean(infection_density_matrix)

# 输出平均值
print(f"感知密度的平均值: {average_awareness_density}")
print(f"感染密度的平均值: {average_infection_density}")
