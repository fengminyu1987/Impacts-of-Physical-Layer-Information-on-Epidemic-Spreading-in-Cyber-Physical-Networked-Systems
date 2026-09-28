import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter

# 1 读取pwi 实验数据
experiment1_df = pd.read_csv('../真实数据—综合比较/1231精简pwi.csv')
# 提取数据
beta_U_exp1 = experiment1_df['beta_U']
rho_I_exp1 = experiment1_df['infection_density']
rho_A_exp1 = experiment1_df['awareness_density']

# 2 读取单纯形 实验数据
experiment2_df = pd.read_csv('../真实数据—综合比较/MC_k=2_加十次平均加进度条版822.csv')
# 提取数据
beta_U_exp2 = experiment2_df['beta_U']
rho_I_exp2 = experiment2_df['infection_density']
rho_A_exp2 = experiment2_df['awareness_density']

#3 读取物理层信息 实验数据
experiment3_df = pd.read_csv('../真实数据—综合比较/MC_PHY info_加十次平均加进度条版822.csv')
# 提取数据
beta_U_exp3 = experiment3_df['beta_U']
rho_A_exp3 = experiment3_df['awareness_density']
rho_I_exp3 = experiment3_df['infection_density']

# 4 读取综合实验数据
experiment4_df = pd.read_csv('../真实数据—综合比较/MC_integrated info_加十次平均加进度条版822.csv')
# 提取数据
beta_U_exp4 = experiment4_df['beta_U']
rho_I_exp4 = experiment4_df['infection_density']
rho_A_exp4 = experiment4_df['awareness_density']

# 5 读取不考虑信息信息传播的实验数据
experiment4_df = pd.read_csv('../真实数据—综合比较/MC_Without Info.csv')
# 提取数据
beta_U_exp5 = experiment4_df['beta_U']
rho_I_exp5 = experiment4_df['infection_density']
rho_A_exp5 = experiment4_df['awareness_density']



# 绘制感染密度曲线
plt.figure(figsize=(10, 6))
plt.plot(beta_U_exp1, rho_I_exp1, 'o-', label='PWI')
plt.plot(beta_U_exp2, rho_I_exp2, 's-', label='2-simplex')
plt.plot(beta_U_exp3, rho_I_exp3, '^-.', label='PHY Info')
plt.plot(beta_U_exp4, rho_I_exp4, 'd:', label='Integrated Info')
plt.plot(beta_U_exp5, rho_I_exp5, 'x--', label='Without Info')

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
plt.xlim(0, 1)
plt.ylim(0, 0.71)
plt.title('')
plt.xlabel('β', fontsize=21)  # 增大x轴标签字体大小
plt.ylabel('$\\rho^{I}$', fontsize=21)  # 增大y轴标签字体大小

# 设置刻度字体大小
plt.xticks(fontsize=19)  # 增大x轴刻度字体大小
plt.yticks(fontsize=19)  # 增大y轴刻度字体大小
# 对于感知密度和感染密度，手动设置 y 轴刻度
plt.yticks(np.arange(0, 0.7, 0.2))  # 每隔 0.1 一个刻度
# 添加网格
plt.grid(True)

# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.96, top=0.95, bottom=0.15)
# 添加图例
plt.legend(fontsize=19)

# 保存图像为PDF
plt.savefig('真实数据_感染密度曲线.pdf', format='pdf')
# 显示图像
plt.show()



# 绘制感知密度曲线
plt.figure(figsize=(10, 6))
plt.plot(beta_U_exp1, rho_A_exp1, 'o-', label='PWI')
plt.plot(beta_U_exp2, rho_A_exp2, 's-', label='2-simplex')
plt.plot(beta_U_exp3, rho_A_exp3, '^-.', label='PHY Info')
plt.plot(beta_U_exp4, rho_A_exp4, 'd:', label='Integrated Info')
plt.plot(beta_U_exp5, rho_I_exp5, 'x--', label='Without Info')

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
plt.xlim(0, 1)
plt.ylim(0, 0.91)
plt.title('')
plt.xlabel('β', fontsize=21)  # 增大x轴标签字体大小
plt.ylabel('$\\rho^{A}$', fontsize=21)  # 增大y轴标签字体大小

# 设置刻度字体大小
plt.xticks(fontsize=19)  # 增大x轴刻度字体大小
plt.yticks(fontsize=19)  # 增大y轴刻度字体大小
# 对于感知密度和感染密度，手动设置 y 轴刻度
plt.yticks(np.arange(0, 0.91, 0.2))  # 每隔 0.1 一个刻度
# 添加网格
plt.grid(True)

# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.1, right=0.96, top=0.95, bottom=0.15)

# 添加图例
plt.legend(fontsize=19)
# 保存图像为PDF
plt.savefig('真实数据_感知密度曲线.pdf', format='pdf')
# 显示图像
plt.show()


