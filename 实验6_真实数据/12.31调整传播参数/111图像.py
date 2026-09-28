import numpy as np
import matplotlib.pyplot as plt

# 定义x的范围
x = np.linspace(0, 1, 400)  # 在0到1之间生成400个点

# 定义theta的值
theta_values = [0.3, 0.5, 0.7]

# 初始化一个图形对象
plt.figure()

# 循环遍历theta的值并绘制对应的函数图像
for theta in theta_values:
    # 计算y的值
    y = 1 / (1 + np.exp(-10 * (x - theta)))
    # 绘制图像
    plt.plot(x, y, label=f'θ = {theta:.1f}')

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('Function $y = 1 - \\frac{1}{1 + \\exp(-10(x - \\theta))}$ for different θ values')
plt.xlabel('x')
plt.ylabel('y')

# 显示图像
plt.show()