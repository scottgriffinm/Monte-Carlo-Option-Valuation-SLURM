import numpy as np
import subprocess
from time import time

def mc_euro_call_controller(S, K, r, sigma, q, T, M, nodes):
	if M % nodes != 0:
		M = M + (nodes - M % nodes)
		print(f"M adjusted to {M} to be evenly divisible by {nodes} nodes.")
	n = int(M/nodes)
	command_list = ['srun', f"-N{nodes}",'python3','mc_euro_call_worker.py', str(S), str(K), str(r), str(sigma), str(q), str(T), str(n), str(M)]
	result = subprocess.run(command_list, capture_output=True, text=True, check=True)
	result = result.stdout.strip()
	result = list(result.splitlines())
	for i in range(len(result)):
		result[i] = float(result[i])
	sum_call = sum(result)
	call_value = np.exp(-r * T) * sum_call
	return call_value

if __name__ == "__main__": 
    start = time()    
    S = 90 	 
    K = 100 	 
    r = 0.05	 
    sigma = 0.2
    q = 0.01  	 
    T = 1   	 
    M = 100_000_000
    nodes = 4
    price = mc_euro_call_controller(S, K, r, sigma, q, T, M, nodes)
    end = time()
    print(f"\nnodes = {nodes}")
    print(f"sims = {M}")
    print(f"time = {round(end-start,6)} seconds")
    print(f"price = {price}\n")



