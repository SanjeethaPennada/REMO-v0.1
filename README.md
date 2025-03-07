# CARLA - Replay with Modifications (REMO)

This repository contains the code to record and replay a scenario with modifications in CARLA. If you find this repository useful, please cite. 

![alt text](https://github.com/SanjeethaPennada/REMO/blob/main/Images/REMO.png)

## Contents
1. [Prerequisites](#Prerequisites)
2. [Setup](#setup)
3. [Scenario Generation](#Scenario-Generation)
4. [Record](#record)
5. [Replay](#replay)
6. [REMO](#REMO (Replay-with-Modifications))

## Prerequisites

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
git clone https://github.com/SanjeethaPennada/REMO.git
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

Install all the required packages from [requirements.txt](https://github.com/SanjeethaPennada/REMO/blob/main/requirements)



## Scenario Generation 
The record and replay functionality is primarily used to streamline the testing of scenarios, eliminating the need for separate scenario-generating files. This approach allows all scenarios to be replayed from a central source, regardless of external folders. To achieve this, a  scenarios was generated from [KING: Generating Safety-Critical Driving Scenarios for Robust Imitation via Kinematics Gradients](https://github.com/autonomousvision/king/tree/main) and executed using Transfuser Autonomous Driving Systems (ADS), which controls the ego vehicle. 

### Running the Code
We provide bash scripts for the experiments for convenience. Please make sure the "CARLA_ROOT" ("./carla_server" by default) and "KING_ROOT" (if present) environment variables are set correctly in all of those scripts. 


## Record

First spin up a carla server in a separate shell:
```Shell
carla_server/CarlaUE4.sh --world-port=2000 -opengl
```

Run the following script in a separate shell: 
```Shell
python3 start_recording.py
```
This should open a Scenario Recorder GUI as shown below to start and stop recording a scenario. 

![alt text](https://github.com/SanjeethaPennada/REMO/blob/main/Images/Scenario_Recorder.png)

Now, open and run the following script in a separate shell to run the scenario: 
```Shell
bash run_generation_transfuser.sh
```
Once the scenario is generated in CARLA - start and stop recording it using Scenario Recorder GUI. The recorded scenario will be saved as test.log.

Close carla server. 

## Replay

Spin up a carla server again in previous shell:
```Shell
carla_server/CarlaUE4.sh --world-port=2000 -opengl
```
#### Scenario replay using .log file
Run the following script in a separate shell: 
```Shell
python3 start_replaying.py
```
This replay uses test.log to replay the recorded scenario. CARLA offers built-in [record and replay](https://carla.readthedocs.io/en/0.9.6/recorder_and_playback/) features, enabling scenarios to be replayed using a `test.log` file. This log captures the behavior of the ego and adversarial vehicles, which can be replayed deterministically. Our objective is to replay the same scenario with modifications such as creating or removing actors, changing traffic light states, or adjusting the number of adversarial vehicles in the simulation. Since the `.log` file is in binary format, it does not allow such modifications. To achieve these modifications, the `.log` file needs to be converted into a more accessible format, such as `.json` file.

#### Convert .log to .json
Run the following script: 
```Shell
python3 log_to_json.py
```
This creates test.json file. Replay the scenario using test.json file by running the following script: 

#### Scenario replay using .json file
Run the following script: 
```Shell
python3 replay_json.py
```

## REMO (Replay with Modifications)
Now, we have got test.jsonDet file that contains ego and adevrsarial vehicles information. 

#### Replay without ego vehicle 
We can remove ego vehicle information from test.json, leaving only the adversarial vehicle data. 

Give the ego vehicle id and run the following script: 
```Shell
python3 remove_ego.py
```
This gives NPC.json which contains adversarial vehicles information only.

Replay scenario to verify if ego vehicle is removed or not by running the following script: 
```Shell
python3 replay_npcs.py
```
This approach allows us to replay the scenario without the ego vehicle (ID=194), ensuring that the NPCs behave deterministically. 

#### Replay with ego vehicle driven by Transfuser
The `NPC.json` file contains information about adversarial vehicles. The `REMO.py` script runs the ego vehicle, which is controlled by the Transfuser ADS (or any other ADS, as needed). It ensures deterministic behavior of the ego vehicle by loading `NPC.json` into the same environment where the ego vehicle is operating.

To generate the scenario run the following script: 
```Shell
bash run_remo.sh
```



## Acknowledgements
This implementation is based on code from several repositories. We sincerely thank the authors for their awesome work.
- [CARLA Leaderboard](https://github.com/carla-simulator/leaderboard)
- [Scenario Runner](https://github.com/carla-simulator/scenario_runner)
- [KING](https://github.com/autonomousvision/king/tree/main)
- [Learning by Cheating](https://github.com/dotchen/LearningByCheating)
- [World on Rails](https://github.com/dotchen/WorldOnRails)
- [Transfuser](https://github.com/autonomousvision/transfuser)
