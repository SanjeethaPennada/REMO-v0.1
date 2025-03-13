#!/usr/bin/env python

import glob
import os
import sys
import time
import json
import carla

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# Initialize CARLA client and world
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

def get_objects_at_location(world, location, radius, label):
    """Retrieve objects of a given label within a specified radius of a location."""
    all_objects = world.get_environment_objects(label)
    return [obj.id for obj in all_objects if location.distance(obj.transform.location) <= radius]

def get_nearby_traffic_and_street_lights(world, location, radius):
    """Retrieve nearby traffic light and street light IDs."""
    entity_ids = {"traffic_light_ids": set(), "street_light_ids": set()}
    
    # Get all actors in the world
    actors = world.get_actors()
    
    # Get traffic light IDs
    for actor in actors:
        if 'traffic_light' in actor.type_id:
            if location.distance(actor.get_transform().location) <= radius:
                entity_ids["traffic_light_ids"].add(actor.id)
    
    # Get street light IDs using Light Manager
    light_manager = world.get_lightmanager()
    all_lights = light_manager.get_all_lights()
    for light in all_lights:
        if location.distance(light.location) <= radius:
            entity_ids["street_light_ids"].add(light.id)
    
    return entity_ids

def monitor_vehicle_spawn_and_record_data(world, vehicle_type, radius=50.0):
    """Monitor the world for ego vehicle spawn and record data for nearby buildings and traffic lights."""
    
    vehicle_found = False
    vehicles = {}

    # Continuously monitor the world for the ego vehicle
    while not vehicle_found:
        actors = world.get_actors()
        for actor in actors:
            if actor.type_id == vehicle_type:
                print(f"Ego vehicle '{vehicle_type}' spawned, starting to track...")
                vehicle_found = True
                vehicles[actor.id] = actor  # Store reference to the vehicle
                break

        time.sleep(0.1)  # Avoid high CPU usage

    # Initialize sets for storing unique IDs
    unique_building_ids = set()
    unique_traffic_light_ids = set()
    unique_street_light_ids = set()

    # Track the ego vehicle's movement and record data
    while True:
        for vehicle in vehicles.values():
            location = vehicle.get_location()
                
            # Retrieve nearby building and light IDs
            building_ids = get_objects_at_location(world, location, radius, carla.CityObjectLabel.Buildings)
            light_ids = get_nearby_traffic_and_street_lights(world, location, radius)
            
            # Add to unique sets
            unique_building_ids.update(building_ids)
            unique_traffic_light_ids.update(light_ids['traffic_light_ids'])
            unique_street_light_ids.update(light_ids['street_light_ids'])

            # Print data to verify
            print(f"Vehicle at {location}, Building IDs: {unique_building_ids}, Traffic Light IDs: {unique_traffic_light_ids}, Street Light IDs: {unique_street_light_ids}")
                
        # Store the collected data periodically
        final_results = {
            'building_ids': list(unique_building_ids),
            'street_light_ids': list(unique_street_light_ids)
        }
        
        # Save to JSON file
        with open('output.json', 'w') as f:
            json.dump(final_results, f, indent=4)
        
        time.sleep(1)  # Wait 1 second before recording again, adjust as necessary

def main():
    vehicle_type = 'vehicle.lincoln.mkz_2017'  # Ego vehicle type

    # Start monitoring vehicle spawn and track data once the vehicle is detected
    monitor_vehicle_spawn_and_record_data(world, vehicle_type)

if __name__ == '__main__':
    main()

