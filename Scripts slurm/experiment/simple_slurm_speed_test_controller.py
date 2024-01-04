import subprocess
from time import time

'''Controller computer script for calculating the average of a number of random numbers.'''

if __name__ == "__main__":
	start = time()	
	iters = 1_000_000_000
	command_list = ['srun','python3','simple_slurm_speed_test_partial.py', f"{iters}"]
	result = subprocess.run(command_list, capture_output=True, text=True, check=True)
	result = result.stdout.strip()
	end = time()
	print(f"random_avg = {result}")
	print(f"time = {round(end-start,6)} seconds")