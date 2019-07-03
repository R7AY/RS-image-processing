from osgeo import gdal_array,gdal, ogr, osr
import shapefile
import pngcanvas


'''阈值化'''
# 输入文件名称
src = "./islands/islands.tif"
# 输出文件名称
tgt = "islands_classified.tif"
# 使用gdal库将图像载入numpy
srcArr =gdal_array.LoadFile(src)
# 将直方图分为20个子区间以便区分
classes = gdal_array.numpy.histogram(srcArr, bins=2)[1]
lut = [[255, 0, 0], [0, 0, 0], [255, 255, 255]]
# 分类的起始值
start = 1
# 建立输出图片
rgb = gdal_array.numpy.zeros((3, srcArr.shape[0], srcArr.shape[1]), gdal_array.numpy.float32)
# 处理所有类别并分配颜色
for i in range(len(classes)):
    mask = gdal_array.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = gdal_array.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i] + 1
# 保存图片
gdal_array.SaveArray(rgb.astype(gdal_array.numpy.uint8), tgt, format="GTIFF", prototype=src)


'''输出shp文件'''
# 阈值化后的输出栅格文件名称
src = "islands_classified.tif"
# 输出的shapefile文件名称
tgt = "extract.shp"
# 图层名称
tgtLayer = "extract"
# 打开输入的栅格文件
srcDS = gdal.Open(src)
# 获取第一个波段
band = srcDS.GetRasterBand(1)
# 让gdal库使用该波段作为遮罩层
mask = band
# 创建输出的shapefile文件
driver = ogr.GetDriverByName("ESRI Shapefile")
shp = driver.CreateDataSource(tgt)
# 拷贝空间索引
srs = osr.SpatialReference()
srs.ImportFromWkt(srcDS.GetProjectionRef())
layer = shp.CreateLayer(tgtLayer, srs=srs)
# 创建dbf文件
fd = ogr.FieldDefn("DN", ogr.OFTInteger)
layer.CreateField(fd)
dst_field = 0
# 从图片中自动提取特征
extract = gdal.Polygonize(band, mask, layer, dst_field, [], None)


'''向shp文件写属性'''
r = shapefile.Reader("extract.shp")
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 800
iheight = 600
xratio = iwidth / xdist
yratio = iheight / ydist
polygons = []

for shape in r.shapes():
    for i in range(len(shape.parts)):
        pixels = []
        pt = None
        if i < len(shape.parts) - 1:
            pt = shape.points[shape.parts[i]:shape.parts[i+1]]
        else:
            pt = shape.points[shape.parts[i]:]
        for x, y in pt:
            px = int(iwidth -((r.bbox[2] - x) * xratio))
            py = int((r.bbox[3] - y) * yratio)
            pixels.append([px, py])
        polygons.append(pixels)
c = pngcanvas.PNGCanvas(iwidth, iheight)
for p in polygons:
    c.polyline(p)
f = open("extract.png", "wb")
f.write(c.dump())
f.close()


