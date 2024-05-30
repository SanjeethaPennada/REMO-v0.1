import carla

def get_street_lights_near_location(world, target_location, radius):
    # Get the light manager
    lmanager = world.get_lightmanager()
    
    # Get all lights in the world
    all_lights = lmanager.get_all_lights()
    
    # Filter and return only the street lights near the target location
    street_lights_near_location = []
    for light in all_lights:
        light_location = light.location
        distance_to_target = light_location.distance(target_location)
        if distance_to_target <= radius:
            street_lights_near_location.append(light)
    return street_lights_near_location

# Connect to the CARLA client
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the world
world = client.load_world('Town03')

# Define the specific location and radius
target_location = carla.Location(x=-20.679825, y=-140.884156, z=0)  #location where collision happened approx
radius = 100.0  # checked till radius of 100

# Get street lights near the specific location
street_lights_near_location = get_street_lights_near_location(world, target_location, radius)

# Print the IDs of street lights near the specific location
print("IDs of Street Lights Near Specific Location:")
for light in street_lights_near_location:
    print("Light ID:", light.id)
