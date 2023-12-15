import numpy as np
import subprocess

def mc_euro_down_and_out_call_controller(S, K, r, sigma, q, T, H, N, total_simulations, workers):
	if total_simulations % workers != 0:
		total_simulations += (workers - total_simulations % workers)
		print(f"Total number of simulations adjusted to {total_simulations} to be evenly divisible by {workers} workers.")
	worker_simulations = int(total_simulations/workers)
	worker_commands = [S, K, r, sigma, q, T, H, N, worker_simulations, total_simulations]
	command_list = ['srun', f"-N{workers}",'python3','mc_euro_down_and_out_call_worker.py']
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
	S = 100
	K = 100
	T = 1
	sigma = 0.2
	r = 0.06
	q = 0.03
	H = 99
	N = 10
	total_simulations = 1_000_000
	workers = 1
	price = mc_euro_down_and_out_call_controller(S, K, r, sigma, q, T, H, N, total_simulations, workers)
	print(f"Workers = {workers}")
	print(f"Total Simulations = {total_simulations}")
	print(f"Price = {price}")
