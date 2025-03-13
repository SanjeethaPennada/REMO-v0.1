import carla
import json

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.get_world()

def get_objects_at_location(world, location, radius, label):
    """Retrieve objects of a given label within a specified radius of a location."""
    all_objects = world.get_environment_objects(label)
    return [obj.id for obj in all_objects if location.distance(obj.transform.location) <= radius]

def get_nearby_traffic_and_street_lights(world, location, radius):
    """Retrieve nearby traffic light and street light IDs."""
    entity_ids = {"traffic_light_ids": set(), "street_light_ids": set()}
    
    # Get all actors in the world
    actors = world.get_actors()
    
    # Get traffic light IDs
    for actor in actors:
        if 'traffic_light' in actor.type_id:
            if location.distance(actor.get_transform().location) <= radius:
                entity_ids["traffic_light_ids"].add(actor.id)
    
    # Get street light IDs using Light Manager
    light_manager = world.get_lightmanager()
    all_lights = light_manager.get_all_lights()
    for light in all_lights:
        if location.distance(light.location) <= radius:
            entity_ids["street_light_ids"].add(light.id)
    
    return entity_ids

# Load vehicle positions from test.json
with open('test.json', 'r') as f:
    vehicle_data = json.load(f)

radius = 50.0  # Define the search radius

# Store unique IDs throughout the journey
unique_building_ids = set()
unique_traffic_light_ids = set()
unique_street_light_ids = set()

# Process only vehicle with ID 194
for frame in vehicle_data['frames']:
    for vehicle in frame['vehicles']:
        if vehicle['id'] == 279:
            location = carla.Location(
                x=vehicle['location']['x'], 
                y=vehicle['location']['y'], 
                z=vehicle['location']['z']
            )
            
            # Retrieve nearby object IDs
            building_ids = get_objects_at_location(world, location, radius, carla.CityObjectLabel.Buildings)
            light_ids = get_nearby_traffic_and_street_lights(world, location, radius)
            
            # Add to unique sets
            unique_building_ids.update(building_ids)
            unique_traffic_light_ids.update(light_ids['traffic_light_ids'])
            unique_street_light_ids.update(light_ids['street_light_ids'])

# Convert sets to lists
final_results = {
    'building_ids': list(unique_building_ids),
    'street_light_ids': list(unique_street_light_ids)
}

# Output the results
with open('output.json', 'w') as f:
    json.dump(final_results, f, indent=4)

print("Data extraction complete. Results saved in output.json.")

