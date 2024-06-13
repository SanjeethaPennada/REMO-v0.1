import carla

def main():
    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    # Load the CARLA world and make required changes
    world = client.load_world('Town03')
    #Get the current CARLA world if trying to incorporate the chnages in the current world
    #world = client.get_world()

    # Define the target locations to remove traffic lights from (97,98,99,100), but remember giving IDs may not work always because continuous running of carla world will change IDs of traffic lights only, so if you are not planning to load carla world for every iteration then try getting the locations of traffic lights using IDs 
    target_locations = [
        carla.Location(x=16.628286, y=-146.755920, z=0.0),
        carla.Location(x=-11.506108, y=-125.105507, z=0.152402),
        carla.Location(x=19.512201, y=-126.721161, z=0.146974),
        carla.Location(x=-12.016109, y=-147.885498, z=0.152402)
    ]

    # Tolerance for location comparison
    location_tolerance = 1.0

    # Get all traffic lights in the world
    traffic_lights = world.get_actors().filter('traffic.traffic_light')

    # Remove traffic lights based on their locations
    for traffic_light in traffic_lights:
        location = traffic_light.get_location()
        for target_location in target_locations:
            if location.distance(target_location) < location_tolerance:
                traffic_light.destroy()
                print("Traffic light at location {} has been removed.".format(location))
                break

if __name__ == '__main__':
    main()
