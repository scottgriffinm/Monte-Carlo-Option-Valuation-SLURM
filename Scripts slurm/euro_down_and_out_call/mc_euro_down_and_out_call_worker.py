import numpy as np
import sys

def mc_euro_down_and_out_call_worker(S, K, r, sigma, q, T, H, N, worker_simulations, total_simulations):
	'''Worker script for pricing a European down-and-out call option using Monte Carlo simulation.
	This script should be located in the /home directory of all SLURM worker computers.'''
	dt = T/N
	nudt = (r - q - 0.5*sigma*sigma)*dt
	sigsdt = sigma * np.sqrt(dt)
	sum_CT = 0
	for i in range(worker_simulations):
		St = S
		BARRIER_CROSSED = False
		for j in range(N):
			e = np.random.randn()
			St = St * np.exp(nudt + sigsdt*e)
			if St <= H:
				BARRIER_CROSSED = True
				break
		if BARRIER_CROSSED:
			CT = 0
		else:
			CT = np.maximum(0, St - K)
		sum_CT += CT
	return sum_CT/total_simulations

if __name__ == "__main__":
	S = float(sys.argv[1]) # Collect arguments from srun command
	K = float(sys.argv[2])
	r = float(sys.argv[3])
	sigma = float(sys.argv[4])
	q = float(sys.argv[5])
	T = int(sys.argv[6])
	H = float(sys.argv[7])
	N = int(sys.argv[8])
	worker_simulations = int(sys.argv[9])
	total_simulations = int(sys.argv[10])
	print(mc_euro_down_and_out_call_worker(S, K, r, sigma, q, T, H, N, worker_simulations, total_simulations))





