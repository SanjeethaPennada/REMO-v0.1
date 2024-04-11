import carla

# Function to set spectator view to a desired location
def set_spectator_location(world, location):
    spectator = world.get_spectator()
    spectator.set_transform(carla.Transform(location, carla.Rotation()))

# Function to get building IDs at a specific location within a radius
def get_building_ids_at_location(world, location, radius):
    # Get environment objects (buildings) in the entire map
    all_buildings = world.get_environment_objects(carla.CityObjectLabel.Buildings)
    
    # Filter buildings within the specified radius of the location
    building_ids = []
    for building in all_buildings:
        building_location = building.transform.location
        distance = location.distance(building_location)
        if distance <= radius:
            building_ids.append(building.id)
    
    return building_ids

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Load "Town03" map
world = client.load_world('Town03')

# Define your location (replace these coordinates with your actual location)
location = carla.Location(x=-80.0, y=100.0, z=100.0)  # Example location -80.0, y=100.0, z=120

# Move the spectator to the specified location
set_spectator_location(world, location)

# Define the radius within which to search for buildings
radius = 150.0  # Adjust the radius as needed 

# Get building IDs at the specified location within the radius
building_ids = get_building_ids_at_location(world, location, radius)

# Define buildings and their IDs as a list
env_objs = world.get_environment_objects(carla.CityObjectLabel.Buildings)
building_objects = [obj for obj in env_objs if obj.id in building_ids]

# Collect the IDs of the first 10 buildings
first_10_building_ids = [building.id for building in building_objects[:10]] 
# Toggle off the first 10 buildings
world.enable_environment_objects(set(first_10_building_ids), False)





#left building (x=-150.0, y=30.0, z=50.0)  , radius = 100, ID [:60] 
#greenery
#right building x=-150.0, y=70.0, z=50.0 , radius = 100, ID [:100]
#top right x=-80.0, y=180.0, z=120.0 , radius = 200, ID [:45]
#top left x=-80.0, y=100.0, z=100.0 , radius = 150, ID [:10]

