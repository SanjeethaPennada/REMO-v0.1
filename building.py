import carla

# Connect to the Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Get the Carla world
world = client.load_world('Town03')

world = client.load_world('Town03_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)

    # Toggle all buildings off
world.unload_map_layer(carla.MapLayer.Buildings)

    # Toggle all buildings on   
#world.load_map_layer(carla.MapLayer.Buildings)
