'''用于对比不同时间的图像变化情况'''

from osgeo import gdal, gdal_array
import numpy as np

# 飓风前影像
img1 = "./before/before.tif"
# 飓风后影像
img2 = "./after/after.tif"

# 将上述图像载入数组
arr1 = gdal_array.LoadFile(img1).astype(np.int8)
arr2 = gdal_array.LoadFile(img2)[1].astype(np.int8)

# 在图片数组上执行差值操作
diff = arr2 - arr1

# 建立类别架构并将变化特征隔离
classes = np.histogram(diff, bins=5)[1]

# 用黑色遮罩不是特变明显的变化特征
lut = [[0, 0, 0], [0, 0, 0], [0, 0, 0],
       [0, 0, 0], [0, 255, 0], [255, 0, 0]]
# 类别初始值
start = 1
# 创建输出图片
rgb = np.zeros((3, diff.shape[0], diff.shape[1], ), np.int8)

# 处理所有类别并配色
for i in range(len(classes)):
    mask = np.logical_and(start <= diff, diff <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = np.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i] + 1

# 保存图片结果
output = gdal_array.SaveArray(rgb, "change.tif", format="GTiff", prototype=img2)
output = None