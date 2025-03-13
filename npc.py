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

# Initialize CARLA client and world
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()


def spawn_vehicles_from_json(world, frame_data, vehicles):
    """Spawn or update NPC vehicles based on the current frame data."""
    
    for vehicle_data in frame_data.get('vehicles', []):
        vehicle_id = vehicle_data['id']
        vehicle_type = vehicle_data['type']
        position = carla.Vector3D(vehicle_data['location']['x'],
                                  vehicle_data['location']['y'],
                                  vehicle_data['location']['z'])
        rotation = carla.Rotation(vehicle_data['rotation']['pitch'],
                                  vehicle_data['rotation']['yaw'],
                                  vehicle_data['rotation']['roll'])
        velocity = carla.Vector3D(vehicle_data['velocity']['x'],
                                  vehicle_data['velocity']['y'],
                                  vehicle_data['velocity']['z'])
        angular_velocity = carla.Vector3D(vehicle_data['angular_velocity']['x'],
                                          vehicle_data['angular_velocity']['y'],
                                          vehicle_data['angular_velocity']['z'])
        if vehicle_id not in vehicles:
            # Find vehicle blueprint
            blueprint = world.get_blueprint_library().find(vehicle_type)
            if not blueprint:
                print(f"Warning: Vehicle type '{vehicle_type}' not found in blueprint library.")
                continue

            vehicle = world.try_spawn_actor(blueprint, carla.Transform(position, rotation))
            if vehicle:
                vehicle.set_target_velocity(velocity)
                vehicle.set_target_angular_velocity(angular_velocity)
                vehicles[vehicle_id] = vehicle
              
        else:
            # Update existing vehicle
            vehicle = vehicles[vehicle_id]
            vehicle.set_transform(carla.Transform(position, rotation))
            vehicle.set_target_velocity(velocity)
            vehicle.set_target_angular_velocity(angular_velocity)


def monitor_vehicle_spawn_and_replay(world, vehicle_type, json_file_path, ego_spawn_location):
    """Monitor the world for ego vehicle spawn at the given location and start the NPC replay."""
    
    # Load the NPC data from JSON file
    with open(json_file_path) as f:
        scenario_data = json.load(f)

    vehicle_found = False
    start_time = None

    # Continuously monitor the world for the ego vehicle at the required position
    while not vehicle_found:
        actors = world.get_actors()
        for actor in actors:
            if actor.type_id == vehicle_type:
                location = actor.get_location()

                # Check if the ego vehicle is at the desired location
                if (abs(location.x - ego_spawn_location.x) < 0.1 and
                    abs(location.y - ego_spawn_location.y) < 0.1 and
                    abs(location.z - ego_spawn_location.z) < 0.1):

                    print(f"Ego vehicle '{vehicle_type}' spawned at required location, starting NPC spawn process...")
                    vehicle_found = True
                    break

        #time.sleep(0.1)  # Avoid high CPU usage

    vehicles = {}  # Store references to spawned NPC vehicles
    processed_frames = set()  # To track executed timestamps
    
    start_time = time.time()
    print(f"NPC spawning will begin at: {start_time}")
    time.sleep(0.1)  # Similar to log_to_json.py

    while True:
        elapsed_time = time.time() - start_time
        elapsed_time_rounded = round(elapsed_time, 4)  # Round elapsed time to 4 decimal places

        for frame in scenario_data['frames']:
            timestamp = round(frame['timestamp'][0], 4)  # Round timestamp to 4 decimal places

            if timestamp not in processed_frames and elapsed_time_rounded == timestamp:
                print(f"Executing frame at timestamp: {timestamp} (Elapsed Time: {elapsed_time_rounded:.4f}s)")
                spawn_vehicles_from_json(world, frame, vehicles)
                processed_frames.add(timestamp)

        if time.time() - start_time > 5.1:  # End the replay after 5.1s
            break


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    vehicle_type = 'vehicle.lincoln.mkz_2017'  # Ego vehicle type
    json_file_path = 'NPC.json'  # Path to NPC scenario file

    # Desired ego vehicle spawn location
    ego_spawn_location = carla.Vector3D(-44.18914794921875, -135.7389678955078, 0.04999999701976776)
#first location of ego vehicle in test.json
    # Start NPC replay once ego vehicle is detected at correct location
    monitor_vehicle_spawn_and_replay(world, vehicle_type, json_file_path, ego_spawn_location)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ending the simulation.")


if __name__ == '__main__':
    main()

