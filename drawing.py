import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 定义绘制六面体的函数
def plot_hexahedron(vertices):
    # 创建 3D 图形对象
    fig = plt.figure()  #画布
    ax = fig.add_subplot(111, projection='3d')  #子图

    # 绘制底面
    ax.plot_surface(np.array(vertices[:4])[:, 0].reshape(2, 2),
                    np.array(vertices[:4])[:, 1].reshape(2, 2),
                    np.array(vertices[:4])[:, 2].reshape(2, 2),
                    alpha=0.5)

    # 绘制顶面
    ax.plot_surface(np.array(vertices[4:])[:, 0].reshape(2, 2),
                    np.array(vertices[4:])[:, 1].reshape(2, 2),
                    np.array(vertices[4:])[:, 2].reshape(2, 2),
                    alpha=0.5)

    # 绘制侧面
    for i in range(4):
        ax.plot_surface(np.array([vertices[i], vertices[(i + 1) % 4],
                                   vertices[(i + 1) % 4 + 4], vertices[i + 4]])[:, 0].reshape(2, 2),
                        np.array([vertices[i], vertices[(i + 1) % 4],
                                  vertices[(i + 1) % 4 + 4], vertices[i + 4]])[:, 1].reshape(2, 2),
                        np.array([vertices[i], vertices[(i + 1) % 4],
                                  vertices[(i + 1) % 4 + 4], vertices[i + 4]])[:, 2].reshape(2, 2),
                        alpha=0.5)

    # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    return ax

# 定义绘制小球的函数
def plot_spheres(ax, centers, radii):
    for center, radius in zip(centers, radii):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
        y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
        z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='r', alpha=0.5)

# 定义六面体的顶点坐标
hexahedron_vertices = [
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # 底面顶点
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # 顶面顶点
]

# 定义小球的中心坐标和半径
sphere_centers = [
    [0.2, 0.3, 0.4],
    [0.6, 0.5, 0.6],
    [0.8, 0.2, 0.7]
]

sphere_radii = [0.1, 0.05, 0.08]

# 绘制六面体
ax = plot_hexahedron(hexahedron_vertices)

# 在六面体内绘制小球
plot_spheres(ax, sphere_centers, sphere_radii)

# 显示图形
plt.show()
