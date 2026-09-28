import time

import networkx as nx

# 定义文件路径
file_path = "./out.opsahl-powergrid_reindexed"

# 初始化无向图
G = nx.Graph()
# 读取文件并构建图
with open(file_path, 'r') as f:
    for line in f:
        # 读取每行数据，假设以空格分隔节点编号
        nodes = line.strip().split()
        if len(nodes) == 2:
            u, v = nodes
            G.add_edge(int(u), int(v))
# 输出图的基本信息
print("图的节点数:", G.number_of_nodes())
print("图的边数:", G.number_of_edges())

for i in range(0, 10000):
    print(i)

time.sleep(10)
print('11012')
# # 保存为 GraphML 格式
# output_path = "./powergrid_graph.graphml"
# nx.write_graphml(G, output_path)
# print("图已保存为:", output_path)