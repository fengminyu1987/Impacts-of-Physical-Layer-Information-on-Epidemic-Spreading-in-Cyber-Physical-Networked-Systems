import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1 读取PWI 实验数据
experiment1_df = pd.read_csv('../实验4_MC热力图/实验41_MC_λ和β热力图/830density_results.csv')
# 提取数据
lambda_info_value = 0.24
df_lambda_info = experiment1_df.loc[experiment1_df['lambda_info'] == lambda_info_value]
# 提取 beta_U 和对应的感知密度和感染密度
beta_U_exp1 = df_lambda_info['beta_U'].values
rho_A_exp1 = df_lambda_info['awareness_density'].values
rho_I_exp1 = df_lambda_info['infection_density'].values


# 2 读取单纯形 实验数据
experiment2_df = pd.read_csv('../实验4_MC热力图/实验42_MC_λ_star和β 热力图/MC_λ_star和β_density.csv')
# 提取数据
lambda_star = 0.24
df_lambda_star = experiment2_df.loc[experiment2_df['lambda_star'] == lambda_star]
# 提取 beta_U 和对应的感知密度和感染密度
beta_U_exp2 = df_lambda_star['beta_U'].values
rho_A_exp2 = df_lambda_star['awareness_density'].values
rho_I_exp2 = df_lambda_star['infection_density'].values

#3 读取物理层信息 实验数据
experiment3_df = pd.read_csv('../实验4_MC热力图/实验43_MC_θ和β热力图/MC_theta和beta_density.csv')
# 提取 theta = 0.24 的数据行
theta_value = 0.76
df_theta = experiment3_df.loc[experiment3_df['theta'] == theta_value]
# 提取 beta_U 和对应的感知密度和感染密度
beta_U_exp3 = df_theta['beta_U'].values
rho_A_exp3  = df_theta['awareness_density'].values
rho_I_exp3 = df_theta['infection_density'].values


# 4 读取综合实验数据
experiment4_df = pd.read_csv('../实验5_综合比较/实验5——MC副本加进度条版813.csv')
# 提取数据
beta_U_exp4 = experiment4_df['beta_U']
rho_I_exp4 = experiment4_df['infection_density']
rho_A_exp4 = experiment4_df['awareness_density']





# 绘制感染密度曲线
plt.figure(figsize=(10, 6))
plt.plot(beta_U_exp1, rho_I_exp1, 'o-', label='PWI')
plt.plot(beta_U_exp2, rho_I_exp2, 's-', label='2-Simplex')
plt.plot(beta_U_exp3, rho_I_exp3, '^-.', label='PHY Info')
plt.plot(beta_U_exp4, rho_I_exp4, 'd:', label='Integrated Info')

# 添加标题和标签
plt.xlim(0, 1)
plt.ylim(0, 0.7)
plt.xlabel('β')
plt.ylabel('ρᴵ')

# 添加网格
plt.grid(True)
# # 添加图例
# plt.legend()
# 保存图像为PDF
#plt.savefig('热力图数据绘_感染密度曲线.pdf', format='pdf')
# 显示图像
plt.show()

# 绘制感知密度曲线
plt.figure(figsize=(10, 6))
plt.plot(beta_U_exp1, rho_A_exp1, 'o-', label='PWI')
plt.plot(beta_U_exp2, rho_A_exp2, 's-', label='2-simplex')
plt.plot(beta_U_exp3, rho_A_exp3, '^-.', label='PHY Info')
plt.plot(beta_U_exp4, rho_A_exp4, 'd:', label='Integrated Info')

# 添加标题和标签
plt.xlim(0, 1)
plt.ylim(0, 0.9)
plt.xlabel('β')
plt.ylabel('ρᴬ')

# 添加网格
plt.grid(True)
# 添加图例
plt.legend()
# 保存图像为PDF
#plt.savefig('热力图数据绘_感知密度曲线.pdf', format='pdf')

# 显示图像
plt.show()
