# Replay of "KING" 

## Requirements

### Hardware
- GPU: NVIDIA Corporation
- Memory: 16GB+
- Storage: 100GB+

### Software
- Ubuntu 20.04
- nvidia driver
- CARLA 0.9.15

## Setup
Clone the repo
```Shell
git clone https://github.com/ADS-Testing/king.git
cd king
```

### Environment
Install drivers and reboot. If the appropriate version of the driver is already installed(Check with the command `nvidia-smi`), you can skip this step.
```Shell
sudo apt update
sudo apt install ubuntu-drivers-common
sudo ubuntu-drivers autoinstall
sudo reboot
```

Install anaconda and build the environment.
```Shell
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
source ~/.profile
conda env create -f environment.yml
conda activate king
```

### Carla
Download and setup CARLA 0.9.15.
```Shell
chmod +x setup_carla.sh
./setup_carla.sh
```

### Transfuser
To generate scenarios for [TransFuser](https://github.com/autonomousvision/transfuser), you need to download the model weights:
```Shell
mkdir -p driving_agents/king/transfuser/model_checkpoints/regular
cd driving_agents/king/transfuser/model_checkpoints/regular
wget https://s3.eu-central-1.amazonaws.com/avg-projects/transfuser/models.zip
unzip models.zip
rm -rf models.zip late_fusion geometric_fusion cilrs aim
cd -
```

## How to run

### Scenario Replay
We provide a bash script for convenience. Please make sure the "CARLA_ROOT" ("./carla_server" by default) and "KING_ROOT" (if present) environment variables are set correctly in all of those scripts.

#### Running the code
For the generation script, first spin up a carla server in a separate shell:
```Shell
carla_server/CarlaUE4.sh --world-port=2000 -RenderOffScreen 
```
If you cannot separate the shell, execute the script in the background.
```Shell
nohup carla_server/CarlaUE4.sh --world-port=2000 -RenderOffScreen &
```
Following script will run generation and automatically evaluate the results.

##### TransFuser generation
For Transfuser generation using both gradient paths, open generate_scenarios.py, change number of agents to 1 or 2 or 4 based on your choice (default = 4 agents) and run:
```Shell
bash run_generation_transfuser.sh
```

#### Getting results
```Shell
generation_results/
├── agents_4
    ├── RouteScenario_136_to_136
    │   ├── results.json
    │   └── scenario_records.json
    ...
    ├── opt.pkl
    └── opt.txt
```

### Scenario Visualization

#### Running the code
First spin up a carla server in a separate shell:
```Shell
carla_server/CarlaUE4.sh --world-port=2000 -RenderOffScreen
```
After providing the directory name you want to visualize as an argument, run the following script. The default directory is set to "generation_results".
```Shell
bash run_visualization.sh generation_results_transfuser
```

#### Getting results
```Shell
generation_results_transfuser/
└── agents_4
    ├── RouteScenario_136_to_136
    │   ├── RouteScenario_112_iter_4.gif
    │   ├── results.json
    │   └── scenario_records.json
   
    ...
    ├── opt.pkl
    └── opt.txt
```

#### Replaying scenario with modifications
Open run_generation_transfuser.sh file, and use below arguments to replay scenario with modification. 
To replay a scenario with modifications, open run_generation_transfuser.sh file, and type below arguments to tailor the environment.

 
a) --building     - to remove all buildings in the Town
b) --building_remove    - to remove specific buildings in the selected scenario. You can also particularly specify which building to be removed by making changes to the building_remove.py file.
c) --trafficlight_remove  - to remove traffic lights in the selected scenario
d) --trafficlight_change  - to change the state of the traffic lights in the selected scenario
e) --weather_afn          - to change weather conditions to afternoon 
f) --weather_mrng         - to change weather to morning 
g) --weather_rain         - to change weather to raining condition
h) --CloudyDawn / --CloudyMorning/ --CloudyNight /--CloudyNoon / --CloudySunset / --Cloudytwilight - Set cloudy weather conditions.
i) --HardRainDawn / --HardRainMorning/ --HardRainNight/ --HardRainNoon/ --HardRainSunset/ --HardRainTwilight - Set hard rain weather conditions.
j) --MidRainDawn/ --MidRainMorning / --MidRainNight / --MidRainNoon /  --MidRainSunset  / --MidRainTwilight - Set medium rain conditions.
k) --SoftRainDawn/ --SoftRainMorning / --SoftRainNight / --SoftRainNoon / --SoftRainSunset/ --SoftRainTwilight - Set soft rain weather conditions.
l) --WetCloudyDawn/ --WetCloudyMorning / --WetCloudyNight/ --WetCloudyNoon/ --WetCloudySunset/ --WetCloudyTwilight  - Set wet cloudy weather conditions.
m) --WetDawn/ --WetMorning / --WetNight / --WetNoon / --WetSunset / --WetTwilight  - Set wet weather conditions.

