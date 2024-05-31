import json
import subprocess
import time
import os
import carla
import random

PASS = 0
FAIL = 1

# Constants
building_ids = [6624907388525486529, 5590853173915701067, 11595376130058892747, 11261989655324469416, 10827724883280509631, 18345568482389893230, 1580899482231826983, 1760263306195875505, 12193930106007007199, 8965582157476607102, 2012950392265273169, 8202849075528332341, 6570133562374327036, 8588501765608435261, 3725429243769496776, 12942124512259043244, 4899373996816986076, 7783727404168196753, 1601677913125771255, 4983866454221917867, 793883526509223864, 11096794554960802340, 18125725892881901402, 9314362118298296807, 10311091484298245286, 12405707544884411272, 14597101749787311194, 1437529571490662170, 160167791312577125, 12317005202958092029, 2630081664371749371, 2795511079265638899, 17619596962267012938, 12253574462247490343, 3709560905934411224]

traffic_light_ids = [97, 98, 99, 100]  # Example traffic light IDs
weather_conditions = ['rain', 'fog', 'cloudy', 'night']  # Example weather conditions
# List of street light IDs to be turned off
ids_to_turn_off = [
    73, 72, 71, 70, 69, 68, 61, 50, 40, 
    24, 26, 25, 27, 130, 456, 440, 305, 301, 
    347, 122, 165, 166, 211, 212, 215, 
    217, 218, 242, 243, 244, 312, 323, 334, 344, 343, 345, 162, 163, 164, 241,
    306, 307, 346]

def ddmin(test, inp, *test_args):
    assert test(inp, *test_args) != FAIL
    
    n = 2
    step_count = 1
    print("Step | Subsequence                              | Error Triggered")
    print("------------------------------------------------------------")
    while len(inp) >= 2:
        start = 0
        subset_length = len(inp) // n
        some_complement_is_failing = False

        while start < len(inp):
            complement = inp[:start] + inp[start + subset_length:]
            error_triggered = test(complement, *test_args) == PASS
            print(f"{step_count:<5} | {complement}{' '*(40-len(str(complement)))}| {'✓' if error_triggered else '❌'}")
            step_count += 1  # Increment step count here
            if error_triggered:
                inp = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(inp):
                break
            n = min(n * 2, len(inp))
     
    return inp

def test_function(inp):
    try:
        collision_rate = get_collision_rate(inp)
        return PASS if collision_rate > 0 else FAIL
    except Exception as e:
        print(f"Error during test: {e}")
        return FAIL

def get_collision_rate(inp):
    # Save test input to a JSON file
    with open('test_input.json', 'w') as f:
        json.dump(inp, f)

    try:
        # Open Carla and run bash script
        os.system("gnome-terminal -- bash -c 'cd carla_server; ./CarlaUE4.sh; exec bash'")

        # Wait for Carla to initialize
        time.sleep(5)
         
        # Execute bash script to get collision rate
        result = subprocess.run(["bash", "run_generation_transfuser.sh"], capture_output=True, text=True)
        output = result.stdout

        collision_rate = None
        for line in output.splitlines():
            if "Collision rate:" in line:
                collision_rate = float(line.split("Collision rate:")[1].strip())
                break

        if collision_rate is None:
            raise ValueError("Collision rate not found in output")

    except Exception as e:
        print(f"Error parsing collision rate: {e}")
        return 0.0
    finally:
        # Close Carla
        os.system("pkill -f CarlaUE4")

    return collision_rate

if __name__ == "__main__":
    # Example usage
    initial_test_input = building_ids + traffic_light_ids + ids_to_turn_off + weather_conditions + [True, True] 
    print(f"Initial Test Input: {initial_test_input}")
    minimal_input = ddmin(test_function, initial_test_input)
    print(f"Minimal failure-inducing input: {minimal_input}")
