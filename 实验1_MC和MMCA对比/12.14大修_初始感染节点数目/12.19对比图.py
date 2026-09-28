import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter


a=10
b=1
print('ab',a,b)
# 读取实验数据
experiment_df = pd.read_csv('916分段.csv')

# 读取理论数据
theory_df = pd.read_csv('实验1_MMCA理论密度12.19.csv')

# 提取数据
beta_U_exp = experiment_df['beta_U']
rho_I_exp = experiment_df['infection_density']
rho_A_exp = experiment_df['awareness_density']

beta_U_theory = theory_df['beta_U']
rho_I_theory = theory_df['infection_density']
rho_A_theory = theory_df['awareness_density']

print('实际a', rho_A_exp)
print('理论a', rho_A_theory)
print('实际a-理论a',rho_A_exp-rho_A_theory )
print('实际a-理论a',abs(rho_A_exp-rho_A_theory))
print('xdwc' , abs(rho_A_exp-rho_A_theory)/abs(rho_A_theory))
print('wc', sum(abs(rho_A_exp-rho_A_theory)/abs(rho_A_theory))/len(rho_A_theory))

# # 仅对分母大于零的元素进行计算
# valid_indices = rho_I_theory > 0  # 找到分母大于零的索引
# # 根据这些索引进行误差计算
# A = abs(rho_I_exp[valid_indices] - rho_I_theory[valid_indices])
# B = sum(A / abs(rho_I_theory[valid_indices]))
print('实际I', rho_I_exp)
print('理论I', rho_I_theory)
print('实际i-理论i', rho_I_exp-rho_I_theory )
A = abs(rho_I_exp-rho_I_theory)
print('实际i-理论i', A)
B = sum(abs(rho_I_exp[9:]-rho_I_theory[9:])/abs(rho_I_theory[9:]))

print('平均感染绝对误差', sum(A)/len(rho_I_theory))
print('平均感知绝对误差', sum(abs(rho_A_exp-rho_A_theory))/len(rho_A_theory))
print('iwc', B/len(rho_I_theory))

# 计算感染密度和感知密度的平均偏差
avg_abs_deviation_I = sum(abs(rho_I_exp - rho_I_theory)) / len(rho_I_theory)
avg_abs_deviation_A = sum(abs(rho_A_exp - rho_A_theory)) / len(rho_A_theory)

# 打印平均偏差
print(f'感染密度的平均偏差: {avg_abs_deviation_I:.6f}')
print(f'感知密度的平均偏差: {avg_abs_deviation_A:.6f}')

# 绘制 密度曲线
plt.figure(figsize=(10, 6))
plt.plot(beta_U_theory, rho_I_theory, color='red', label='ρᶦ(MMCA)', linewidth=2)
plt.plot(beta_U_theory, rho_A_theory, color='red', linestyle='--', label='ρᴬ(MMCA)', linewidth=2)

plt.plot(beta_U_exp, rho_I_exp, color='blue', marker='+', label='ρᶦ(MC)', linewidth=2) #color='red', linestyle='--', linewidth=1
plt.plot(beta_U_exp, rho_A_exp, color='blue', marker='+', linestyle='--', label='ρᴬ(MC)', linewidth=2)


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
plt.xlabel('β', fontsize=14)  # 增大x轴标签字体大小
plt.ylabel('ρ', fontsize=14)  # 增大y轴标签字体大小

# 设置刻度字体大小
plt.xticks(fontsize=12)  # 增大x轴刻度字体大小
plt.yticks(fontsize=12)  # 增大y轴刻度字体大小

# 添加网格
plt.grid(True)
# 添加图例
plt.legend(fontsize=12)

# 调整图形的边距以减少空白
plt.subplots_adjust(left=0.07, right=0.96, top=0.95, bottom=0.1)





# # 保存图像为PDF
# plt.savefig('实验1_mc与mmca密度对比.pdf', format='pdf')
# 显示图像
plt.show()
