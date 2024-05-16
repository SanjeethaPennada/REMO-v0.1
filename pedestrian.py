
 
import carla
import random
import time

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)



# Load the CARLA world
#world = client.load_world('Town03')

# Get the world object
world = client.get_world()

# Define the spawn location for the pedestrian
spawn_location = carla.Location(x=-67.599852, y=10.541729, z=0.792587)

# Get the blueprint library and choose a random walker blueprint
blueprint_library = world.get_blueprint_library()
walker_bp = random.choice(blueprint_library.filter('walker.pedestrian.*'))

# Spawn the pedestrian at the specified location
pedestrian = world.spawn_actor(walker_bp, carla.Transform(spawn_location))

# Set the target location for the pedestrian to walk towards
target_location = carla.Location(x=-67.699852, y=-10.541729, z=0.792587)

# Create a controller for the pedestrian
pedestrian_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
pedestrian_controller = world.spawn_actor(pedestrian_controller_bp, carla.Transform(), attach_to=pedestrian)

# Set the target location for the pedestrian controller
pedestrian_controller.start()
pedestrian_controller.go_to_location(target_location)

# Sleep for a short duration to allow the pedestrian to start walking
time.sleep(10)

# Check if the pedestrian is walking
if pedestrian_controller.is_active():
    print("Pedestrian is walking towards the target location.")
else:
    print("Pedestrian is not walking. There might be an issue.")

# Sleep for a longer duration to allow time for the pedestrian to reach the target location
time.sleep(110)

# Stop the pedestrian controller
pedestrian_controller.stop()

# Destroy the pedestrian and controller
pedestrian.destroy()
pedestrian_controller.destroy()
