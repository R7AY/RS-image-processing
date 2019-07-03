from osgeo import gdal_array

# 源图片的名称
src = "FalseColor.tif"
# 将源图片载入到数组中
arr = gdal_array.LoadFile(src)
# 交换波段1和波段2的位置，使用“高级分片”功能直接对波段进行重新排列
output = gdal_array.SaveArray(arr[[1, 0, 2], :], "swap.tif", format="GTiff",prototype=src)
# 取消输出，避免在某些平台上损坏文件
output = None
