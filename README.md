HARDWARE
    GPU: NVIDIA Tesla T4
    Memory: 16GB+
    Storage: 150GB+

SOFTWRAE
    Ubuntu 20.04
    nvidia driver
    CARLA 0.9.15
    
Setup
	Clone the repo
	git clone https://github.com/SanjeethaPennada/King-Replay.git
        cd King-Replay
        

Environment
	Install drivers and reboot. If the appropriate version of the driver is already  installed(Check with the command nvidia-smi), you can skip this step.

	sudo apt update
	sudo apt install ubuntu-drivers-common
	sudo ubuntu-drivers autoinstall
	sudo reboot
	
Install anaconda and build the environment.
	wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
source ~/.profile
conda env create -f environment.yml
conda activate King-Replay

Carla

	Download and setup CARLA 0.9.15.

	chmod +x setup_carla.sh
	./setup_carla.sh
	

Transfuser
	
 To generate scenarios for TransFuser, you need to download the model weights:

	mkdir -p driving_agents/king/transfuser/model_checkpoints/regular
	cd driving_agents/king/transfuser/model_checkpoints/regular
	wget https://s3.eu-central-1.amazonaws.com/avg-projects/transfuser/models.zip
	unzip models.zip
	rm -rf models.zip late_fusion geometric_fusion cilrs aim
	cd -
	
How to run
	Scenario Generation
	We provide bash script for the experiments for convenience. Please make sure the "CARLA_ROOT" ("./carla_server" by default) and "KING-REPLAY_ROOT" (if present) environment variables are set correctly in all of those scripts.
	
For the generation script, first spin up a carla server in a separate shell:

carla_server/CarlaUE4.sh --world-port=2000 -RenderOffScreen

If you cannot separate the shell, execute the script in the background.

nohup carla_server/CarlaUE4.sh --world-port=2000 -RenderOffScreen &

Following scripts will run generation.
TransFuser generation
	For Transfuser generation using both gradient paths, run:

	bash run_generation_transfuser.sh

Getting results

generation_results/
└── agents_4
    ├── RouteScenario_112_to_112
    │   ├── results.json
    │   └── scenario_records.json
    ...
    ├── opt.pkl
    └── opt.txt
    

Scenario Visualization
	Running the code

	First spin up a carla server in a separate shell:

	carla_server/CarlaUE4.sh --world-port=2000 -RenderOffScreen

	After providing the directory name you want to visualize as an argument, run the following script. The default directory is set to "generation_results".

	bash run_visualization.sh generation_results_transfuser
	
	
Getting results

generation_results_transfuser/
└── agents_4
    ├── RouteScenario_112_to_112
    │   ├── RouteScenario_112_iter_4.gif
    │   ├── results.json
    │   └── scenario_records.json
    ├── RouteScenario_114_to_114
    │   ├── RouteScenario_114_iter_1.gif
    │   ├── results.json
    │   └── scenario_records.json
    ...
    ├── opt.pkl
    └── opt.txt

We would like to recreate a single scenario, so select any route/scenario which you would like to replicate, lets suppose its RouteScenario_136_to_136, so go to leaderboard/data/routes/subset_20perTown and remoe all unwanted routes except the one you desire. Also, change iter = 1 in run_generation_transfuser.sh file. Now run 

bash run_generation_transfuser.sh  - it runs only RouteScenario_136_to_136, visualize it using ash run_visualization.sh generation_results_transfuser


Note: From driving_agents/king/aim_bev/king_initializations/initializations_subset - both agents 1 and 2 are copied to driving_agents/king/transfuer/king_initializations/initializations_subset (this can be done becuase all agents are similar) 


By changing number of agents in run_generation_transfuser.sh i.e., 'num_agents 2' the number of adversial agents changes to 2, and similarly for 1 too. 
Constraint: There is no data with number of adversial agents = 3. 




		

	
