import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the CARLA world
world = client.get_world()

# Get all traffic lights in the world
traffic_lights = world.get_actors().filter("*traffic_light*")

# Change the state of each traffic light
for traffic_light in traffic_lights:
    # Get the traffic light's state
    traffic_light_state = traffic_light.get_state()
    
    # Change the state of the traffic light (for example, to Green)
    if traffic_light_state != carla.TrafficLightState.Green:
        traffic_light.set_state(carla.TrafficLightState.Green)

