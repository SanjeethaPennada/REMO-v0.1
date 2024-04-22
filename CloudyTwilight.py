import carla

def set_weather(world, weather):
    world.set_weather(weather)

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.get_world()

# Define weather parameters 
weather = carla.WeatherParameters()
weather.cloudiness = 80.0
weather.precipitation = 0.0
weather.precipitation_deposits = 0.0
weather.wind_intensity = 0.35
weather.sun_azimuth_angle = 135.0  # Adjust as needed
weather.sun_altitude_angle = 0.0  # Adjust as needed to simulate early morning
weather.fog_density = 0.0
weather.fog_distance = 0.0
weather.fog_falloff = 0.0
weather.wetness = 0.0
#weather.time_of_day = 7.0  # Adjust as needed to simulate early morning (e.g., 7.0 for 7 AM)

# Set the weather conditions
set_weather(world, weather)

