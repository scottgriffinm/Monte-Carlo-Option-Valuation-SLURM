import numpy as np
import sys

def mc_asian_call_control_variate_worker(S, K, sigma, r, q, T, N, worker_simulations, total_simulations):
	dt = T/N
	nudt = (r - q - 0.5 * sigma * sigma) * dt
	sigsdt = sigma * np.sqrt(dt)
	sum_CT = 0
	normal_samples = np.random.normal(size=N)
	for i in range(worker_simulations):
		St = S 
		sumSt = 0
		productSt = 1
		for j in range(N):
			e = normal_samples[j]
			St = St * np.exp(nudt + sigsdt * e)
			sumSt += St
			productSt = productSt * St
		A = sumSt / N
		G = productSt ** (1 / N)
		CT = max(A - K, 0) - max(G - K, 0)
		sum_CT = sum_CT + CT
	return sum_CT / total_simulations

if __name__ == "__main__":
    S = float(sys.argv[1])
    K = float(sys.argv[2])
    r = float(sys.argv[3])
    sigma = float(sys.argv[4])
    q = float(sys.argv[5])
    T = int(sys.argv[6])
    N = int(sys.argv[7])
    worker_simulations = int(sys.argv[8])
    total_simulations = int(sys.argv[9])
    print(mc_asian_call_control_variate_worker(S, K, sigma, r, q, T, N, worker_simulations, total_simulations))



