import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Load the CARLA world
world = client.load_world('Town03')

# Get all traffic lights in the world
traffic_lights = world.get_actors().filter("*traffic_light*")

# Store the IDs of traffic lights
 #Remember giving IDs may not work always because continuous running of carla world will change IDs of traffic lights only, so if you are not planning to load carla world for every iteration then try getting the locations of traffic lights using IDs, and if you are loading CARLA world for every iteration directly rmeove traffic lights using IDs
traffic_light_ids = [97,98,99,100]

# Retrieve IDs of traffic lights
for traffic_light in traffic_lights:
    traffic_light_ids.append(traffic_light.id)

# Remove all traffic lights
for traffic_light in traffic_lights:
    traffic_light.destroy()

# Print the IDs of the removed traffic lights
print("IDs of removed traffic lights:", traffic_light_ids)
