from osgeo import gdal
from osgeo import osr 
from osgeo import ogr

def convert_utm_to_wgs84(easting, northing):
    utm_zone = 36  # UTM Zone 36N
    utm_band = 'N'  # Northern Hemisphere
    
    # Create UTM to WGS84 geographic coordinate transformation
    utm_srs = osr.SpatialReference()
    utm_srs.ImportFromEPSG(32636)
    # utm_srs.SetWellKnownGeogCS("WGS84")
    # utm_srs.SetUTM(utm_zone, True)
    # utm_srs.SetUTMZone(utm_zone, utm_band)
    
    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)  # EPSG code for WGS84
    
    transform = osr.CoordinateTransformation(utm_srs, wgs84_srs)
    
    # Create a point geometry with UTM coordinates
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(easting, northing)
    point.Transform(transform)
    
    # Get the converted WGS84 geographic coordinates
    lat, lon, _ = point.GetPoint()
    
    return lon, lat

# Path to the input and output text files
input_file = 'coord_list.txt'
output_file = 'output.txt'

lines_to_skip = 2
i=0
# Open the input file for reading and the output file for writing
with open(input_file, 'r') as input_file, open(output_file, 'w') as output_file:
    # Read each line in the input file
    for line in input_file:
        if i < lines_to_skip:
            i = i+1
            continue

        easting, northing = map(float, line.strip().split())
        
        # Convert UTM coordinates to WGS84 geographic coordinates
        lon, lat = convert_utm_to_wgs84(easting, northing)
        
        # Write the converted coordinates to the output file
        output_file.write(f'{lon:.6f} {lat:.6f}\n')
        # output_file.write(f'WGS84 Lon: {lon:.6f}, Lat: {lat:.6f}\n')
