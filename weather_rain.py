import carla

def set_weather(world, weather):
    world.set_weather(weather)

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.get_world()

# Define weather parameters for night and rain
weather = carla.WeatherParameters()
weather.cloudiness = 80.0
weather.precipitation = 80.0
weather.precipitation_deposits = 80.0
weather.wind_intensity = 50.0
weather.sun_azimuth_angle = 90.0
weather.sun_altitude_angle = -90.0  # Setting negative altitude to simulate night
weather.fog_density = 0.8
weather.fog_distance = 50.0
weather.fog_falloff = 2.0
weather.wetness = 1.0
weather.time_of_day = 0.0  # Setting time_of_day to 0.0 to simulate night

# Set the weather conditions
set_weather(world, weather)



