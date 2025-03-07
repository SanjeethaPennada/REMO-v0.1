#!/usr/bin/env python

import glob
import os
import sys
import time
import json

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

def is_position_occupied(world, location, threshold=2.0):
    """Check if a position is occupied by another vehicle within a given threshold."""
    actors = world.get_actors().filter('vehicle.*')
    for actor in actors:
        if actor.get_location().distance(location) < threshold:
            return True
    return False

def set_spectator_view(world, target_vehicle):
    """Attach spectator view to a vehicle."""
    spectator = world.get_spectator()
    transform = target_vehicle.get_transform()
    spectator_transform = carla.Transform(
        transform.location + carla.Location(z=10, x=-10),
        transform.rotation
    )
    spectator.set_transform(spectator_transform)

def spawn_vehicles_from_json(world, json_data):
    vehicles = {}
    ego_vehicle = None

    for frame in json_data['frames']:
        timestamp = frame['timestamp']
        data = frame['vehicles']
        
        for vehicle_data in data:
            vehicle_id = vehicle_data['id']
            vehicle_type = vehicle_data['type']
            position = carla.Location(**vehicle_data['location'])
            rotation = carla.Rotation(**vehicle_data['rotation'])
            
            if vehicle_id in vehicles:
                vehicles[vehicle_id].set_transform(carla.Transform(position, rotation))
            else:
                blueprint = world.get_blueprint_library().find(vehicle_type)
                if not blueprint:
                    continue

                attempts = 5
                while is_position_occupied(world, position) and attempts > 0:
                    position.z += 0.5
                    attempts -= 1

                vehicle = world.try_spawn_actor(blueprint, carla.Transform(position, rotation))
                if vehicle:
                    vehicles[vehicle_id] = vehicle
                    if ego_vehicle is None:
                        ego_vehicle = vehicle
                        set_spectator_view(world, ego_vehicle)

        time.sleep(0.1)

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town03')

    # Load JSON and spawn vehicles
    json_file_path = 'test.json'
    with open(json_file_path) as f:
        scenario_data = json.load(f)
    spawn_vehicles_from_json(world, scenario_data)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ending the simulation.")

if __name__ == '__main__':
    main()
