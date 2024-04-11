import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the CARLA world
world = client.get_world()

# Get all traffic lights in the world
traffic_lights = world.get_actors().filter("*traffic_light*")

# Remove all traffic lights
for traffic_light in traffic_lights:
    traffic_light.destroy()

