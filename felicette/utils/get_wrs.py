import ogr
import shapely.wkt
import shapely.geometry

# define shapefile
shapefile = 'felicette/assets/landsat-path-row/WRS2_descending.shp'
wrs = ogr.Open(shapefile)

def check_point(feature, point, mode):
    geom = feature.GetGeometryRef() #Get geometry from feature
    shape = shapely.wkt.loads(geom.ExportToWkt()) #Import geometry into shapely to easily work with our point
    if point.within(shape) and feature['MODE']==mode:
        return True
    else:
        return False

def get_wrs_dict(lon, lat):
    point = shapely.geometry.Point(lon, lat)
    layer = wrs.GetLayer(0)
    # ascend or descent
    mode = 'D'
    i=0
    while not check_point(layer.GetFeature(i), point, mode):
        i += 1
    feature = layer.GetFeature(i)
    path = feature['PATH']
    row = feature['ROW']
    return {'path': path, 'row': row}
