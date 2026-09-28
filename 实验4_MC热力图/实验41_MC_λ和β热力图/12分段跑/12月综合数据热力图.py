#
# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
# import random
# import pandas as pd
# import itertools
# from matplotlib.ticker import FuncFormatter
#
#
# # 从 CSV 文件读取数据
# df = pd.read_csv('综合数据.csv')
#
# # 提取 lambda_info 和 lambda_info 的唯一值
# lambda_info_values = np.unique(df['lambda_info'])
# beta_values = np.unique(df['beta_U'])
#
#
# # 创建热力图矩阵
# awareness_density_matrix = df.pivot(index='lambda_info', columns='beta_U', values='awareness_density').values
# infection_density_matrix = df.pivot(index='lambda_info', columns='beta_U', values='infection_density').values
#
# # 自定义截断函数，只保留前4位数
# def truncate_values(matrix, decimal_places=3):
#     factor = 10 ** decimal_places  # 用于控制截断的位数
#     return np.floor(matrix * factor) / factor  # 乘以10的4次方，然后用floor去掉后面的位数
#
# # 对感知密度和感染密度矩阵进行截断处理，只保留前 4 位数
# awareness_density_matrix = truncate_values(awareness_density_matrix, 3)
# infection_density_matrix = truncate_values(infection_density_matrix, 3)
#
#
# #绘制热力图
# plt.figure(figsize=(14, 6))
# plt.subplot(1, 2, 1)
# plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
# plt.colorbar()
# plt.title('Awareness Density Heatmap')
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\lambda_{info}$')
# plt.subplot(1, 2, 2)
# plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
# plt.colorbar()
# plt.title('830_Infection Density Heatmap')
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\lambda_{info}$')
# plt.tight_layout()
# plt.show()
#
#
# # 对数据应用高斯平滑
# plt.figure(figsize=(10, 6))
# # 平滑后的感知密度热力图
# #plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
# plt.imshow(awareness_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
#
# # 自定义格式化函数，将 0.0 显示为 0
# def custom_formatter(x, pos):
#     if x == 0:
#         return '0'
#     else:
#         return '{:.1f}'.format(x)
# # 使用自定义的格式化函数来格式化刻度标签
# ax = plt.gca()
# ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))
# ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))
# # 添加标题和标签
# plt.xlabel('$\\beta$', fontsize=21)  # 增大x轴标签字体大小
# plt.ylabel('$\\lambda$', fontsize=21)  # 增大y轴标签字体大小
# # 设置刻度字体大小
# plt.xticks(fontsize=19)  # 增大x轴刻度字体大小
# plt.yticks(fontsize=19)  # 增大y轴刻度字体大小
# cbar = plt.colorbar()
# # 设置颜色条刻度字体大小为19
# cbar.ax.tick_params(labelsize=19)
# # 获取颜色条的最小值和最大值
# vmin = cbar.vmin
# vmax = cbar.vmax
#
# # # 设置颜色条的刻度为每隔0.2一个刻度，并使用 vmax 作为结束值
# cbar.set_ticks(np.arange(0, vmax+0.01 , 0.2))  # +0.2 确保包含 vmax
# cbar.ax.set_title('$\\rho^{A}$', pad=10, fontsize=21)  # 在色标上方添加标题
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\lambda$')
# # 调整图形的边距以减少空白
# plt.subplots_adjust(left=0.1, right=0.96, top=0.95, bottom=0.15)
# plt.tight_layout()
# plt.savefig('mc感知λ和β热力图.pdf', format='pdf')
# # plt.savefig('实验4_mc感知λstar和β热力图.pdf', format='pdf', bbox_inches='tight')
# plt.show()
#
#
# ##### 平滑后的感染密度热力图
# plt.figure(figsize=(10, 6))
# #plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
# plt.imshow(infection_density_matrix, cmap='jet', aspect='auto', origin='lower',extent=[0, 1, 0, 1], interpolation='gaussian')
# # 自定义格式化函数，将 0.0 显示为 0
# def custom_formatter(x, pos):
#     if x == 0:
#         return '0'
#     else:
#         return '{:.1f}'.format(x)
# # 使用自定义的格式化函数来格式化刻度标签
# ax = plt.gca()
# ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))
# ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))
#
# # 添加标题和标签
# plt.xlabel('$\\beta$', fontsize=21)  # 增大x轴标签字体大小
# plt.ylabel('$\\lambda$', fontsize=21)  # 增大y轴标签字体大小
#
# # 设置刻度字体大小
# plt.xticks(fontsize=19)  # 增大x轴刻度字体大小
# plt.yticks(fontsize=19)  # 增大y轴刻度字体大小
#
# cbar = plt.colorbar()
# # 设置颜色条刻度字体大小为19
# cbar.ax.tick_params(labelsize=19)
# # 获取颜色条的最小值和最大值
# vmin = cbar.vmin
# vmax = cbar.vmax
#
# # 设置颜色条的刻度为每隔0.2一个刻度，并使用 vmax 作为结束值
# cbar.set_ticks(np.arange(0, vmax+0.01 , 0.2))  # +0.2 确保包含 vmax
#
# cbar.ax.set_title('$\\rho^{I}$', pad=10, fontsize=21)  # 在色标上方添加标题
# plt.xlabel('$\\beta$')
# plt.ylabel('$\\lambda$')
# # 调整图形的边距以减少空白
# plt.subplots_adjust(left=0.1, right=0.96, top=0.95, bottom=0.15)
# plt.tight_layout()
# plt.savefig('mc感染λ和β热力图.pdf', format='pdf')
# plt.show()
#
# # 计算感知密度的平均值
# average_awareness_density = np.mean(awareness_density_matrix)
#
# # 计算感染密度的平均值
# average_infection_density = np.mean(infection_density_matrix)
#
# # 输出平均值
# print(f"感知密度的平均值: {average_awareness_density}")
# print(f"感染密度的平均值: {average_infection_density}")
#


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 读取 CSV 文件
df = pd.read_csv('综合数据.csv')

# 获取 lambda_info 和 beta_U 在步长为 0.04 的数据
lambda_info_values = np.arange(0, 1.04, 0.04)  # lambda_info 取值范围 0 到 1，步长为 0.04
beta_U_values = np.arange(0, 1.04, 0.04)  # beta_U 取值范围 0 到 1，步长为 0.04

# 筛选出 lambda_info 和 beta_U 满足步长为0.04的数据
filtered_data = df[df['lambda_info'].isin(lambda_info_values) & df['beta_U'].isin(beta_U_values)]

# 计算 awareness_density 和 infection_density 的平均值
awareness_mean = filtered_data['awareness_density'].mean()
infection_mean = filtered_data['infection_density'].mean()

print(f"筛选后的 lambda_info 和 beta_U 步长为 0.04，awareness_density 和 infection_density 的平均值为: {awareness_mean}, {infection_mean}")

# 创建热力图矩阵
awareness_density_matrix = filtered_data.pivot(index='lambda_info', columns='beta_U', values='awareness_density').values
infection_density_matrix = filtered_data.pivot(index='lambda_info', columns='beta_U', values='infection_density').values

# 自定义截断函数，只保留前4位数
def truncate_values(matrix, decimal_places=3):
    factor = 10 ** decimal_places  # 用于控制截断的位数
    return np.floor(matrix * factor) / factor  # 乘以10的3次方，然后用floor去掉后面的位数

# 对感知密度和感染密度矩阵进行截断处理，只保留前 3 位数
awareness_density_matrix = truncate_values(awareness_density_matrix, 3)
infection_density_matrix = truncate_values(infection_density_matrix, 3)

# 绘制热力图
plt.figure(figsize=(14, 6))

# 绘制感知密度热力图
plt.subplot(1, 2, 1)
plt.imshow(awareness_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('Awareness Density Heatmap')
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda_info$')

# 绘制感染密度热力图
plt.subplot(1, 2, 2)
plt.imshow(infection_density_matrix, origin='lower', aspect='auto', extent=[0, 1, 0, 1], cmap='hot')
plt.colorbar()
plt.title('Infection Density Heatmap')
plt.xlabel('$\\beta$')
plt.ylabel('$\\lambda_info$')

plt.tight_layout()
plt.show()

# 对数据应用高斯平滑
plt.figure(figsize=(10, 6))

# 平滑后的感知密度热力图
plt.imshow(awareness_density_matrix, cmap='jet', aspect='auto', origin='lower', extent=[0, 1, 0, 1], interpolation='gaussian')

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
plt.xlabel('$\\beta$', fontsize=21)
plt.ylabel('$\\lambda$', fontsize=21)

# 设置刻度字体大小
plt.xticks(fontsize=19)
plt.yticks(fontsize=19)

cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=19)

# 获取颜色条的最小值和最大值
vmin = cbar.vmin
vmax = cbar.vmax

# 设置颜色条的刻度为每隔0.2一个刻度，并使用 vmax 作为结束值
cbar.set_ticks(np.arange(vmin, vmax + 0.01, 0.2))

cbar.ax.set_title('$\\rho^{A}$', pad=10, fontsize=21)
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('MC_Awareness_Heatmap_Step_0.04.pdf', format='pdf')
plt.show()

# 平滑后的感染密度热力图
plt.figure(figsize=(10, 6))
plt.imshow(infection_density_matrix, cmap='jet', aspect='auto', origin='lower', extent=[0, 1, 0, 1], interpolation='gaussian')

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
plt.xlabel('$\\beta$', fontsize=21)
plt.ylabel('$\\lambda$', fontsize=21)

# 设置刻度字体大小
plt.xticks(fontsize=19)
plt.yticks(fontsize=19)

cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=19)

# 获取颜色条的最小值和最大值
vmin = cbar.vmin
vmax = cbar.vmax

# 设置颜色条的刻度为每隔0.2一个刻度，并使用 vmax 作为结束值
cbar.set_ticks(np.arange(vmin, vmax + 0.01, 0.2))

cbar.ax.set_title('$\\rho^{I}$', pad=10, fontsize=21)
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
plt.tight_layout()
plt.savefig('MC_Infection_Heatmap_Step_0.04.pdf', format='pdf')
plt.show()

# 计算感知密度的平均值，感染密度的平均值
average_awareness_density = np.mean(awareness_density_matrix)
average_infection_density = np.mean(infection_density_matrix)

# 输出平均值
print(f"感知密度的平均值: {average_awareness_density}")
print(f"感染密度的平均值: {average_infection_density}")
