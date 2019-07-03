import cv2
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread("./input.TIF")

#初始化卷积核
kernels = [
    (u"低通滤波器", np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]]) * 0.1), # 平滑算法（椒盐噪声-中值滤波 高斯噪声-均值滤波）
    (u"高通滤波器", np.array([[0.0, -1, 0], [-1, 5, -1], [0, -1, 0]])), # 锐化算法（sobel算子 roberts算子）
    (u"边缘检测", np.array([[-1.0, -1, -1], [-1, 8, -1], [-1, -1, -1]]))# 垂直，水平检测
]

index = 0

fig, axes = plt.subplots(1, 3, figsize=(12, 4.3))

for ax, (name, kernel) in zip(axes, kernels):
    dst = cv2.filter2D(src, -1, kernel)
    ax.imshow(dst[:, :, ::-1])
    ax.set_title(name)
    ax.axis('off')

fig.subplots_adjust(0.02, 0, 0.98, 1, 0.02, 0)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.show()