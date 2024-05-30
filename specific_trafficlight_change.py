import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Load the CARLA world
world = client.load_world('Town03')


# Define the IDs of the traffic lights you want to change their state
traffic_light_ids = [97,98,99,100]  # Replace with the IDs of the traffic lights you want to change

# Change the state of each traffic light by its ID
for traffic_light_id in traffic_light_ids:
    # Get the traffic light actor
    traffic_light = world.get_actor(traffic_light_id)
    
    if traffic_light is not None:
        # Change the state of the traffic light (for example, to Green)
        traffic_light.set_state(carla.TrafficLightState.Green)
        print("Changed state of traffic light with ID {} to Green.".format(traffic_light_id))
    else:
        print("Traffic light with ID {} not found.".format(traffic_light_id))
