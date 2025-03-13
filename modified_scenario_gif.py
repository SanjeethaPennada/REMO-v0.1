#!/usr/bin/env python

import carla
import cv2
import numpy as np
import time
import imageio

# Initialize CARLA client and world
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

def capture_frames(camera, frame_limit=300):
    """Capture frames from the camera and save them to create a GIF."""
    frames = []
    count = 0

    # Start capturing frames
    def process_image(image):
        nonlocal count
        if count < frame_limit:
            # Convert the image from CARLA format to OpenCV format
            image_data = np.array(image.raw_data).reshape((image.height, image.width, 4))[:, :, :3]
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)
            frames.append(image_data)  # Store the frame
            count += 1
        else:
            # Stop capturing after the frame limit is reached
            camera.stop()

    # Start listening to the camera
    camera.listen(process_image)
    try:
        while count < frame_limit:
            time.sleep(0.1)  # Sleep a little to ensure frames are captured
    except KeyboardInterrupt:
        print("Capture interrupted.")
        camera.stop()

    return frames

def create_gif_from_frames(frames, gif_filename="output.gif", duration=0.1):
    """Create a GIF from the captured frames."""
    with imageio.get_writer(gif_filename, mode='I', duration=duration) as writer:
        for frame in frames:
            writer.append_data(frame)  # Add each frame to the GIF
    print(f"GIF saved as {gif_filename}")

def main():
    # Wait for ego vehicle to spawn
    vehicle_type = 'vehicle.lincoln.mkz_2017'
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

    # Capture frames for a certain period (for example, 300 frames)
    frames = capture_frames(camera, frame_limit=300)

    # Create the GIF from the captured frames
    create_gif_from_frames(frames, gif_filename="modified_scenario.gif", duration=0.1)

if __name__ == '__main__':
    main()

