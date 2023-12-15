import numpy as np
import subprocess

def mc_euro_call_controller(S, K, r, sigma, q, T, total_simulations, workers):
	if total_simulations % workers != 0:
		total_simulations = total_simulations + (workers - total_simulations % workers)
		print(f"Total number of simulations adjusted to {total_simulations} to be evenly divisible by {workers} workers.")
	worker_simulations = int(total_simulations/workers)
	worker_commands = [S, K, r, sigma, q, T, worker_simulations, total_simulations]
	command_list = ['srun', f"-N{workers}",'python3','mc_euro_call_worker.py']
	for i in range(len(worker_commands)):
		command_list.append(str(worker_commands[i]))
	result = subprocess.run(command_list, capture_output=True, text=True, check=True)
	result = result.stdout.strip()
	result = list(result.splitlines())
	for i in range(len(result)):
		result[i] = float(result[i])
	sum_call = sum(result)
	return np.exp(-r * T) * sum_call

if __name__ == "__main__":   
    S = 90 
    K = 100 	 
    r = 0.05	 
    sigma = 0.2
    q = 0.01  	 
    T = 1   	 
    total_simulations = 10_000_000 
    workers = 4
    price = mc_euro_call_controller(S, K, r, sigma, q, T, total_simulations, workers)
    print(f"\nWorkers = {workers}")
    print(f"Total Simulations = {total_simulations}")
    print(f"Price = {price}\worker_simulations")



