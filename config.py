import carla
import json

# Define function to read IDs from output.json
def read_ids_from_json(json_file):
    """Reads building and streetlight IDs from a given JSON file."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Extract building and streetlight IDs from the JSON
        building_ids = data.get('building_ids', [])
        streetlight_ids = data.get('streetlight_ids', [])
        return building_ids, streetlight_ids
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return [], []

# Function to retrieve all street lights in the world
def get_street_lights(world):
    """Retrieves all street lights in the CARLA world."""
    lmanager = world.get_lightmanager()
    all_lights = lmanager.get_all_lights()
    street_lights = [light for light in all_lights if light.light_group == carla.LightGroup.Street]
    return street_lights

# Function to turn off street lights by their IDs
def turn_off_lights_by_ids(lights, streetlight_ids):
    """Turns off the street lights by their IDs."""
    for light in lights:
        if light.id in streetlight_ids:
            light.turn_off()
            print(f"Street light with ID {light.id} has been turned off.")

# Function to configure the environment
def configure_environment(building_ids, streetlight_ids):
    """Configures the CARLA simulation environment based on the input configuration."""
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    # Remove specified buildings
    for building_id in building_ids:
        world.enable_environment_objects({building_id}, False)
        print(f"Building with ID {building_id} has been removed.")
    
    # Turn off specified street lights
    street_lights = get_street_lights(world)
    turn_off_lights_by_ids(street_lights, streetlight_ids)

    world.tick()

# Main function to execute the configuration
if __name__ == "__main__":
    # Load IDs from output.json
    building_ids, streetlight_ids = read_ids_from_json('output.json')

    # Configure the environment based on the loaded IDs
    configure_environment(building_ids, streetlight_ids)

