import carla
import random


building_ids = [6624907388525486529, 5590853173915701067, 11595376130058892747, 11261989655324469416, 10827724883280509631, 18345568482389893230, 1580899482231826983, 1760263306195875505, 12193930106007007199, 8965582157476607102, 2012950392265273169, 8202849075528332341, 6570133562374327036, 8588501765608435261, 3725429243769496776, 12942124512259043244, 4899373996816986076, 7783727404168196753, 1601677913125771255, 4983866454221917867, 793883526509223864, 11096794554960802340, 18125725892881901402, 9314362118298296807, 10311091484298245286, 12405707544884411272, 14597101749787311194, 1437529571490662170, 160167791312577125, 12317005202958092029, 2630081664371749371, 2795511079265638899, 17619596962267012938, 12253574462247490343, 3709560905934411224]

traffic_light_ids = [97, 98, 99, 100]  # Example traffic light IDs
weather_conditions = ['rain', 'fog', 'cloudy', 'night']  # Example weather conditions

# List of street light IDs to be turned off
ids_to_turn_off = [
    73, 72, 71, 70, 69, 68, 61, 50, 40,
    24, 26, 25, 27, 130, 456, 440, 305, 301,
    347, 122, 165, 166, 211, 212, 215,
    217, 218, 242, 243, 244, 312, 323, 334, 344, 343, 345, 162, 163, 164, 241,
    306, 307, 346
]

# Function to set weather conditions
def set_weather_conditions(world, weather_conditions):
    weather = carla.WeatherParameters()

    # Initialize default weather parameters, if the test input contains the list of weather_conditions, then the below are executed, or else default settings will be executed.
    weather.precipitation = 0.0
    weather.precipitation_deposits = 0.0
    weather.wind_intensity = 0.20
    weather.fog_density = 0.0
    weather.fog_distance = 0.0
    weather.fog_falloff = 0.0
    weather.cloudiness = 90.0
    weather.sun_azimuth_angle = 135
    weather.sun_altitude_angle = 35

    # Apply specified weather conditions
    if 'rain' in weather_conditions:
        weather.precipitation = 30.0
        weather.precipitation_deposits = 50.0
        weather.wind_intensity = 50.40

    if 'fog' in weather_conditions:
        weather.fog_density = 0.8
        weather.fog_distance = 50.0
        weather.fog_falloff = 2.0

    if 'cloudy' in weather_conditions:
        weather.cloudiness = 20.0

    if 'night' in weather_conditions:
        weather.sun_azimuth_angle = 270.0
        weather.sun_altitude_angle = -80.0

    world.set_weather(weather)

# Function to retrieve all street lights in the given CARLA world
def get_street_lights(world):
    lmanager = world.get_lightmanager()
    all_lights = lmanager.get_all_lights()
    street_lights = [light for light in all_lights if light.light_group == carla.LightGroup.Street]
    return street_lights

# Function to turn off street lights by their IDs
def turn_off_lights_by_ids(lights, ids_to_turn_off):
    for light in lights:
        if light.id in ids_to_turn_off:
            light.set_intensity(0.0)

# Function to spawn a bike at a specific location
def spawn_bike(world, spawn_location=carla.Location(x=-20.679825, y=-140.884156, z=0)):
    blueprint_library = world.get_blueprint_library()
    bike_blueprints = blueprint_library.filter('vehicle.harley-davidson.low_rider')
    if bike_blueprints:
        bike_bp = random.choice(bike_blueprints)
        bike = world.spawn_actor(bike_bp, carla.Transform(spawn_location))
        return bike
    else:
        print("No bike blueprints available.")
        return None

# Function to spawn a pedestrian at a specific location and make them walk to a target location
def spawn_pedestrian(world, spawn_location=carla.Location(x=-20.599852, y=-120.541729, z=0.792587), target_location=carla.Location(x=-40.599852, y=-140.541729, z=0.792587)):
    blueprint_library = world.get_blueprint_library()
    walker_bp = random.choice(blueprint_library.filter('walker.pedestrian.*'))
    pedestrian = world.spawn_actor(walker_bp, carla.Transform(spawn_location))
    
    pedestrian_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
    pedestrian_controller = world.spawn_actor(pedestrian_controller_bp, carla.Transform(), attach_to=pedestrian)
    
    pedestrian_controller.start()
    pedestrian_controller.go_to_location(target_location)
    
    return pedestrian, pedestrian_controller

def configure_environment(inp):
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town03')

    # Remove specified buildings
    for building_id in building_ids:
        if building_id in inp:
            world.enable_environment_objects({building_id}, False)
            print(f"Building with ID {building_id} has been removed.")

    # Remove specified traffic lights
    for traffic_light_id in traffic_light_ids:
        if traffic_light_id in inp:
            traffic_light = world.get_actor(traffic_light_id)
            if traffic_light:
                traffic_light.destroy()
                print(f"Traffic light with ID {traffic_light_id} has been removed.")

    # Set weather conditions
    relevant_conditions = [condition for condition in weather_conditions if condition in inp]
    if relevant_conditions:
        set_weather_conditions(world, relevant_conditions)

    # Get all street lights
    street_lights = get_street_lights(world)
    for light_id in ids_to_turn_off:
        if light_id in inp:
            turn_off_lights_by_ids(street_lights, [light_id])
            print(f"Street light with ID {light_id} has been turned off.")

    # Spawn bike if True is in the input list
    if 'Bike' in inp:
        spawn_bike(world)

    # Spawn pedestrian if True is in the input list
    if 'Pedestrain' in inp:
        spawn_pedestrian(world)

    # Save world changes
    world.tick()

import json

if __name__ == "__main__":
    # Usage with test input from a JSON file, reads input from test_input.json and configure environment accordingly and execute scenario under similar settings
    with open('test_input.json', 'r') as f:
        test_input_from_file = json.load(f)
    
    print(f"Test Input from file: {test_input_from_file}")
    configure_environment(test_input_from_file)
