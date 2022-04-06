from math import radians, cos, sin, asin, sqrt, degrees, pi, atan2

_AVG_EARTH_RADIUS_KM = 6371.0088

# Following code is originated from haversine library: https://github.com/mapado/haversine
def calculateDistanceInKM(point1, point2):
    """ Calculate the great-circle distance between two points on the Earth surface in km.
    Takes two 2-tuples, containing the latitude and longitude of each point in decimal degrees.
    :param point1: first point; tuple of (latitude, longitude) in decimal degrees
    :param point2: second point; tuple of (latitude, longitude) in decimal degrees
    Example:
        lyon = (45.7597, 4.8422)        # lat, long
        paris = (48.8567, 2.3508)       # lat, long

        print("Distance: {}".format(calculateDistanceInKM(lyon, paris)))
    """

    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

    return 2 * _AVG_EARTH_RADIUS_KM * asin(sqrt(d))

def find_location(lat, long, LOCATIONS):
    num_loc = len(LOCATIONS)
    assert num_loc > 0, "Please provide a LOCATIONS array!"
    min_dist = float('inf')
    min_loc = None
    for k, v in LOCATIONS.items():
        cur_dist = calculateDistanceInKM((lat, long), v)
        if cur_dist < min_dist:
            min_dist = cur_dist
            min_loc = k
    return min_loc