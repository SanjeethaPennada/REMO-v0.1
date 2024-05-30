import carla

def get_street_lights(world):
    # Get the light manager
    lmanager = world.get_lightmanager()
    
    # Get all lights in the world
    all_lights = lmanager.get_all_lights()
    
    # Filter and return only the street lights
    street_lights = [light for light in all_lights if light.light_group == carla.LightGroup.Street]
    return street_lights

# Connect to the CARLA client
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the desired world
world = client.load_world('Town03')

# Get all street lights
street_lights = get_street_lights(world)


# Print the IDs of street lights
print("IDs of Street Lights:")
for light in street_lights:
    print("Light ID:", light.id)