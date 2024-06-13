import carla

def main():
    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    # Load the CARLA world
    world = client.load_world('Town03')
    #Get the current CARLA world if trying to incorporate the chnages in the current world
    #world = client.get_world()
    
    # Get the blueprint library
    blueprint_library = world.get_blueprint_library()

    # Get all traffic lights in the world
    traffic_lights = world.get_actors().filter('traffic.traffic_light')
    #Remember giving IDs may not work always because continuous running of carla world will change IDs of traffic lights only, so if you are not planning to load carla world for every iteration then try getting the locations of traffic lights using IDs  
    
    # Define a list to store the locations of the traffic lights
    traffic_light_locations = []

    # Iterate through all traffic lights and get their locations

    for traffic_light in traffic_lights:
        location = traffic_light.get_location()
        traffic_light_locations.append((traffic_light.id, location))
        print("Traffic light ID: {}, Location: {}".format(traffic_light.id, location))

    #Traffic light IDs to be removed
    traffic_light_ids_to_remove = [97, 100, 98, 99]

    # Remove specified traffic lights
    for traffic_light_id in traffic_light_ids_to_remove:
        traffic_light = world.get_actor(traffic_light_id)
        if traffic_light is not None:
            traffic_light.destroy()
            print("Traffic light with ID {} has been removed.".format(traffic_light_id))
        else:
            print("Traffic light with ID {} not found.".format(traffic_light_id))

    # Disable environment objects for the specified traffic lights
    world.enable_environment_objects(set(traffic_light_ids_to_remove), False)

if __name__ == '__main__':
    main()
