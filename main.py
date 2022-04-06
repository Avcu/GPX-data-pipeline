import os
import json
import gpxpy
import gpxpy.gpx
from datetime import datetime

from functions import *

_OUTPUT_LEN = 60
_RUN_KM_H_THRESHOLD = 12
_RUN_KM_THRESHOLD = 10

LOCATIONS = {"LA, USA": (34.01842, -118.29528), "Ankara, TR": (39.86538, 32.74836), "Manisa, TR": (38.73484, 27.56861)}

path_this = os.getcwd()
src_path = os.path.join("my_geo_data", "all")
src_full_path = os.path.join(path_this, src_path)

# STEP-0
print("="*_OUTPUT_LEN)
print("STEP-0")
print("-"*_OUTPUT_LEN)
print("Looking for gpx files in the following path: {}".format(src_full_path))
gpx_files = [f for f in os.listdir(src_full_path) if f.endswith('.gpx')]

if len(gpx_files)==0:
    assert 1==0, "No gpx files have been found, please try another source directory"
else:
    print("{} gpx files have been found!".format(len(gpx_files)))
print("-"*_OUTPUT_LEN)

# STEP-1
print("="*_OUTPUT_LEN)
print("STEP-1")
print("-"*_OUTPUT_LEN)
print("Iterating through the detected gpx files...")

num_file = len(gpx_files)
track_data = {}
for file_idx in range(num_file): # num_file
    track_data[file_idx] = {}
    track_data[file_idx]['file_name'] = gpx_files[file_idx]
    print('-- File number :{} and name: {}'.format(file_idx, gpx_files[file_idx]))

    # load the data
    cur_gpx_file = open(os.path.join(src_full_path, gpx_files[file_idx]), 'r')
    cur_gpx = gpxpy.parse(cur_gpx_file)

    # iterate through tracks
    track_data[file_idx]['tracks'] = []
    for track in cur_gpx.tracks:

        # iterate through segments
        for segment in track.segments:
            segment_dict = {}

            tot_time = 0
            tot_distance = 0
            segment_dict['points'] = []
            for point_idx, point in enumerate(segment.points):
                # print('Point at ({},{},{}) -> time: {}'.format(point.latitude, point.longitude, point.elevation, point.time))
                segment_dict['points'].append((point.latitude, point.longitude, point.time.timestamp()))

                # find the location from a location array based on the initial point
                if point_idx == 0:
                    loc_ = find_location(point.latitude, point.longitude, LOCATIONS)

                # calculate the distance and elapsed time from the previous point to current point
                if point_idx>0:
                    prev_point = segment.points[point_idx-1]
                    dist_ = calculateDistanceInKM((prev_point.latitude, prev_point.longitude), (point.latitude, point.longitude))
                    time_ = point.time.timestamp() - prev_point.time.timestamp()
                    # print("---> Distance in m: {} and elapsed time: {}".format(dist_*1000, time_))

                    tot_distance += dist_
                    tot_time += time_

            segment_dict['location'] = loc_
            segment_dict['tot_distance_km'] = tot_distance
            segment_dict['tot_time_min'] = tot_time/60
            segment_dict['ave_speed_km_h'] = tot_distance/(tot_time/3600)
            if segment_dict['ave_speed_km_h'] > _RUN_KM_H_THRESHOLD or segment_dict['tot_distance_km'] > _RUN_KM_THRESHOLD:
                segment_dict['type'] = 'biking'
            else:
                segment_dict['type'] = 'running'

            track_data[file_idx]['tracks'].append(segment_dict)

            print("Location: {}".format(loc_))
            print("Total distance in km: {} and total time in min: {}, average speed: {} km/h".format(tot_distance, tot_time/60, tot_distance/(tot_time/3600)))

# STEP-2
print("="*_OUTPUT_LEN)
print("STEP-2")
print("-"*_OUTPUT_LEN)
print("Save the dictionary as a JSON file.")

with open("track_data.json", "w") as f:
    json.dump(track_data, f)

print("Data is saved as a JSON file.")

# STEP-3
print("="*_OUTPUT_LEN)
print("STEP-3")
print("-"*_OUTPUT_LEN)
print("Create KML file...")

running_kml = create_kml_str(track_data, type='running')
biking_kml = create_kml_str(track_data, type='biking')

print("Saving the KML file...")
with open("tracks_run.kml", "w") as f:
    f.write(running_kml)
with open("tracks_bike.kml", "w") as f:
    f.write(biking_kml)
print("KML file is saved")


