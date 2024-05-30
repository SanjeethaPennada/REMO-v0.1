import carla

def get_street_lights(world):
    """
    Retrieve all street lights in the given CARLA world.
    """
    lmanager = world.get_lightmanager()
    all_lights = lmanager.get_all_lights()
    street_lights = [light for light in all_lights if light.light_group == carla.LightGroup.Street]
    return street_lights

def turn_off_lights_by_ids(lights, ids_to_turn_off):
    """
    Turn off lights whose IDs are in the ids_to_turn_off list by setting their intensity to 0.
    """
    for light in lights:
        if light.id in ids_to_turn_off:
            light.set_intensity(0.0)

def set_weather(world, weather):
    """
    Set the weather parameters in the given CARLA world.
    """
    world.set_weather(weather)

# Connect to the CARLA client
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the desired world
world = client.load_world('Town03')

# Define and set the weather parameters
weather = carla.WeatherParameters(
    cloudiness=20.0,
    precipitation=0.0,
    precipitation_deposits=50.0,
    wind_intensity=0.35,
    sun_azimuth_angle=90.0,  # Adjust as needed
    sun_altitude_angle=0.0,  # Adjust as needed to simulate early morning
    fog_density=0.0,
    fog_distance=0.0,
    fog_falloff=0.0,
    wetness=0.0
)
set_weather(world, weather)

# Get all street lights
street_lights = get_street_lights(world)


# List of street light IDs to be turned off

ids_to_turn_off = [
    73, 72, 71, 70, 69, 68, 61, 50, 40, 
    24, 26, 25, 27, 130, 456, 440, 305, 301, 
    347, 122, 165, 166, 211, 212, 215, 
    217, 218, 242, 243, 244, 312, 323, 334, 344, 343,345, 162, 163, 164,  241,
    306, 307, 346]


# Print the IDs of street lights
print("IDs of Street Lights:")
for light in street_lights:
    print("Light ID:", light.id)

# Turn off the specified street lights
turn_off_lights_by_ids(street_lights, ids_to_turn_off)

print("Specified street lights turned off.")
