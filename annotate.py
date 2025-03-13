#!/usr/bin/env python

import json
import carla
import cv2
import numpy as np
import time

# Initialize CARLA client and world
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

def calculate_distance(loc1, loc2):
    """Calculate the Euclidean distance between two locations."""
    return np.sqrt((loc1.x - loc2.x)**2 + (loc1.y - loc2.y)**2 + (loc1.z - loc2.z)**2)

def project_to_2d(camera, world_location):
    """Project 3D world location to 2D screen space using CARLA's camera projection."""
    try:
        # Get the camera intrinsic matrix
        intrinsic = np.array(camera.calibration_matrix)

        # Get the camera transform
        cam_transform = camera.get_transform()
        world_to_camera = np.array(cam_transform.get_matrix())

        # Convert world coordinates to camera coordinates
        world_coords = np.array([world_location.x, world_location.y, world_location.z, 1.0])
        camera_coords = np.dot(world_to_camera, world_coords)

        # Ignore objects behind the camera
        if camera_coords[2] <= 0:
            return None, None

        # Convert to pixel space
        x = int((camera_coords[0] / camera_coords[2]) * intrinsic[0, 0] + intrinsic[0, 2])
        y = int((camera_coords[1] / camera_coords[2]) * intrinsic[1, 1] + intrinsic[1, 2])

        # Check if within image bounds
        image_w, image_h = int(camera.attributes['image_size_x']), int(camera.attributes['image_size_y'])
        if 0 <= x < image_w and 0 <= y < image_h:
            return x, y
        return None, None

    except Exception as e:
        print(f"Error projecting to 2D: {e}")
        return None, None

def process_image(image, camera, building_locations, streetlight_locations, vehicle_location):
    """Annotate the image with object IDs and save the final frame."""
    image_data = np.array(image.raw_data).reshape((image.height, image.width, 4))[:, :, :3]
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)

    annotated = False

    for bid, loc in building_locations.items():
        # Calculate distance from the vehicle to the building
        if calculate_distance(vehicle_location, loc) <= 50.0:
            x, y = project_to_2d(camera, loc)
            if x and y:
                cv2.putText(image_data, f"BID: {bid}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                print(f"Annotated Building ID {bid} at ({x}, {y})")  # Debugging output
                annotated = True

    for sid, loc in streetlight_locations.items():
        # Calculate distance from the vehicle to the streetlight
        if calculate_distance(vehicle_location, loc) <= 50.0:
            x, y = project_to_2d(camera, loc)
            if x and y:
                cv2.putText(image_data, f"SID: {sid}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                print(f"Annotated Street Light ID {sid} at ({x}, {y})")  # Debugging output
                annotated = True

    if annotated:
        print("Objects successfully annotated.")
    else:
        print("No objects were annotated.")

    cv2.imwrite('annotated_image.png', image_data)
    cv2.imshow('Annotated Image', image_data)
    cv2.waitKey(1)

def capture_and_annotate_continuously(world, camera, building_locations, streetlight_locations, vehicle_location):
    """Continuously capture images and annotate visible objects."""
    camera.listen(lambda image: process_image(image, camera, building_locations, streetlight_locations, vehicle_location))

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping simulation.")
        cv2.destroyAllWindows()

def monitor_vehicle_spawn_and_annotate(world, vehicle_type, camera):
    """Monitor for ego vehicle spawn and continuously fetch location.json."""
    vehicle_found = False

    while not vehicle_found:
        print("Checking for ego vehicle...")
        for actor in world.get_actors():
            if actor.type_id == vehicle_type:
                print(f"Ego vehicle '{vehicle_type}' spawned.")
                vehicle_found = True
                break
        time.sleep(0.5)

    ego_vehicle = next(actor for actor in world.get_actors() if actor.type_id == vehicle_type)
    vehicle_location = ego_vehicle.get_location()

    while True:  # Continuously reload locations
        with open('location.json', 'r') as f:
            data = json.load(f)
            building_locations = {bid: carla.Location(**loc) for bid, loc in data.get('buildings', {}).items()}
            streetlight_locations = {sid: carla.Location(**loc) for sid, loc in data.get('street_lights', {}).items()}

        print(f"Loaded {len(building_locations)} buildings and {len(streetlight_locations)} streetlights from location.json.")
        
        capture_and_annotate_continuously(world, camera, building_locations, streetlight_locations, vehicle_location)
        time.sleep(5)  # Reload location.json every 5 seconds

def main():
    vehicle_type = 'vehicle.lincoln.mkz_2017'

    # Wait for ego vehicle to spawn
    while True:
        actors = world.get_actors()
        ego_vehicle = next((actor for actor in actors if actor.type_id == vehicle_type), None)
        if ego_vehicle:
            print(f"Ego vehicle '{vehicle_type}' found.")
            break
        time.sleep(1)

    # Attach the camera to the vehicle
    camera_transform = carla.Transform(carla.Location(x=0, y=0, z=3), carla.Rotation(pitch=-15))
    blueprint = world.get_blueprint_library().find('sensor.camera.rgb')
    camera = world.spawn_actor(blueprint, camera_transform, attach_to=ego_vehicle)

    monitor_vehicle_spawn_and_annotate(world, vehicle_type, camera)

if __name__ == '__main__':
    main()

