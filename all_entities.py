import carla
import random
# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Load the CARLA world
world = client.get_world()
#world = client.get_world()
def set_weather(world, weather):
    world.set_weather(weather)
weather = carla.WeatherParameters()
weather.cloudiness = 20.0
weather.precipitation = 0.0
weather.precipitation_deposits = 50.0
weather.wind_intensity = 0.35
weather.sun_azimuth_angle = 90.0  # Adjust as needed
weather.sun_altitude_angle = 0.0  # Adjust as needed to simulate early morning
weather.fog_density = 0.0
weather.fog_distance = 0.0
weather.fog_falloff = 0.0
weather.wetness = 0.0
set_weather(world, weather)
# Define a list of traffic light IDs to remove (reweplace with your IDs)
traffic_light_ids_to_remove = [97,98,99,100] # Example IDs, replace with your own 69, 80,107,108
for traffic_light_id in traffic_light_ids_to_remove:
    traffic_light = world.get_actor(traffic_light_id)
    if traffic_light is not None:
        traffic_light.destroy()
        print("Traffic light with ID {} has been removed.".format(traffic_light_id))
    else:
        print("Traffic light with ID {} not found.".format(traffic_light_id))

# Define the IDs of the buaaeildings to remove
buildings_to_remove_ids=[6624907388525486529, 5590853173915701067, 11595376130058892747, 11261989655324469416, 10827724883280509631, 18345568482389893230, 1580899482231826983, 1760263306195875505, 12193930106007007199, 8965582157476607102, 2012950392265273169, 8202849075528332341, 6570133562374327036, 8588501765608435261, 3725429243769496776, 12942124512259043244, 4899373996816986076, 7783727404168196753, 1601677913125771255, 4983866454221917867, 793883526509223864, 11096794554960802340, 18125725892881901402, 9314362118298296807, 10311091484298245286, 12405707544884411272, 14597101749787311194, 1437529571490662170, 160167791312577125, 12317005202958092029, 2630081664371749371, 2795511079265638899, 17619596962267012938, 12253574462247490343, 3709560905934411224]
import time

# Function to spawn a bike at a specific location
import random
import time


world.enable_environment_objects(set(buildings_to_remove_ids), False)
