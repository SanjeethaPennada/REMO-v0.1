import carla

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the CARLA world
world = client.get_world()

# Get the traffic light with ID 69
traffic_light = world.get_actor(98)

# Change the state of the traffic light to stop
if traffic_light:
    traffic_light.set_state(carla.TrafficLightState.Red)
