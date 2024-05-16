import carla
import random
import time

# Function to spawn a bike at a specific location
def spawn_bike(world, spawn_location):
    blueprint_library = world.get_blueprint_library()
    bike_blueprints = blueprint_library.filter('vehicle.harley-davidson.low_rider')
    if bike_blueprints:
        bike_bp = random.choice(bike_blueprints)
        bike = world.spawn_actor(bike_bp, carla.Transform(spawn_location))
        return bike
    else:
        print("No bike blueprints available.")
        return None

# Function to control the bike's movement
def control_bike(bike):
    bike.apply_control(carla.VehicleControl(throttle=0.4, steer=0.0))

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()


# Load the CARLA world
    #world = client.load_world('Town03')




    # Define the spawn location for the bike
    spawn_location = carla.Location(x=-80.679825, y=1.284156, z=0.5)  # Adjust as needed

    # Spawn the bike
    bike = spawn_bike(world, spawn_location)
    if bike:
        print("Bike spawned successfully.")
        
        # Control the bike's movement
        control_bike(bike)

        # Keep the bike running for 120 seconds
        time.sleep(120)

        # Destroy the bike actor
        bike.destroy()
        print("Bike destroyed.")
    else:
        print("Failed to spawn bike.")

except Exception as e:
    print("Error:", e)


 
 