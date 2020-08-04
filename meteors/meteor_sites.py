## Tasks to get done:
# 1 - Get data
# 2 - Convert to data struct
# 3 - Calculate distance
# 4 - Sort data by distance
# 5 - Select 10 closests sites, and print the data

import requests
from math import radians, cos, sin, asin, sqrt 

### Local lat/long:

fred_lat = 38.3032
fred_long = -77.4605

###

### Request meteor impact sites from data.nasa.gov

def get_meteor_sites():
    meteor_response = requests.get(
        'https://data.nasa.gov/resource/gh4g-9sfh.json',
        params={'$limit': 50000}
    )

    meteor_data = meteor_response.json()
    return meteor_data

###

### Python 3 program to calculate Distance Between Two Points on Earth 

def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers (6371). Use 3956 for miles 
    r = 3956
       
    # calculate the result 
    return(c * r) 
      
###      

### Take list of meteor sites, return list with additional key for distance

def insert_distance_key(input_list):
    working_data = list()
    for embedded_dict in input_list:
        try:
            current_lat = float(embedded_dict['reclat'])
            current_long = float(embedded_dict['reclong'])

            # Calculate meteor site distance from Fredericksburg
            dist_from_fred = distance(
                    fred_lat, 
                    current_lat, 
                    fred_long, 
                    current_long
                    )
            
            # Add distance key to embedded dictionary
            embedded_dict['distance'] = dist_from_fred

            # Add embedded dictionary to working data
            working_data.append(embedded_dict)

        except KeyError:
            ## Used for debugging:
            #print('KeyError found in dictionary with name {0}'.format(embedded_dict['name']))
            continue
        except:
            print('Something went wrong')
            raise
    
    # Return the Working Dictionary
    return working_data

###

### Sort by distance

def sort_by_distance(sort_embedded_dict):
    return sort_embedded_dict['distance']

###

if __name__ == '__main__':
    meteor_data = get_meteor_sites()

    distance_list = insert_distance_key(meteor_data)

    distance_list.sort(key=sort_by_distance)

    print('')
    print('A list of Metoer Sites near Fredericksburg, VA:')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for site in range(10):
        print('The {0} site is {1} miles away'.format(
            distance_list[site]['name'],
            distance_list[site]['distance'])
            )