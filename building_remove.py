import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.load_world('Town03')


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



# Define your location (replace these coordinates with your actual location)
location = carla.Location(x=-150.0, y=30.0, z=50.0)  # top left
#location = carla.Location(x=-150.0, y=70.0, z=50.0)  # bottom left
#location = carla.Location(x=-80.0, y=100.0, z=100.0)  # top right
#location = carla.Location(x=-80.0, y=180.0, z=120.0)  # bottom right

# Move the spectator to the specified location
set_spectator_location(world, location)

# Define the radius within which to search for buildings
radius = 400.0  # top left
#radius = 100.0  # bottom left
#radius = 150.0  # top right
#radius = 200.0  # bottom right


# Get building IDs at the specified location within the radius
building_ids = get_building_ids_at_location(world, location, radius)

# Define buildings and their IDs as a list
env_objs = world.get_environment_objects(carla.CityObjectLabel.Buildings)
building_objects = [obj for obj in env_objs if obj.id in building_ids]

# Collect the IDs of the first n buildings
#first_n_building_ids = [building.id for building in building_objects[:50]] # top left 

#backtwin[1562699237605548669, 17235122108563265677, 12495691760231386670, 16313181619495315148, 17798064116822404580] 
#fronttwin[15844954996823609767, 11645801049091093097, 10649589213450182065, 8176918256333549158, 6579379009551399333] [15730254308531548549, 12261070413986386661], 
#[10188087204226691652, 3561252634485631611, 15238124405572899009, 8794281533802726069, 16547936984919951199, 15730254308531548549, 12261070413986386661, 8732043879944152783, 5506737825174028137]frontred, 
#[6030282197145637780, 8809622762887559187,10324585425144648710] backright 
#[5436003053874918619] front left

#first_n_building_ids = [building.id for building in building_objects[:100]]  #bottom left

#[14667240896428621566] [7989182760411716713],[7434222945297012083], [6119766853874817756], [5190909769548762716],[7787089966138231893], [8496972126047413161], [1847028611639114807, 18238141741817433176, 11649272373429102199, 17588387645644995256, 5943620872444923320, 3723439850461389687, 15621887747340052088]


#first_n_building_ids = [building.id for building in building_objects[:20]]  # top right

#15291547881600329180, 14108779543167826866,16411497468756660201,10556292272449826464, 6985771807368227206, 15412060631299303716, 1865729148775104458, 14545706866894736195, 17859665951547599284, 9625298279031795291, 6468839090202963001


first_n_building_ids = [building.id for building in building_objects[:500]] # bottom right



# Toggle off the first 10 buildings
world.enable_environment_objects(set(first_n_building_ids), False)
print("Building ID of removed building:", first_n_building_ids)


