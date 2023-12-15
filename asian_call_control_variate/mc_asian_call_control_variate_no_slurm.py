import numpy as np
from scipy.stats import norm

def black_scholes_euro_call(S, K, r, sigma, q, T):
	d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
	d2 = d1 - sigma * np.sqrt(T)
	call_value = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
	return call_value

def geometric_asian_call(S, K, r, sigma, q, T, N):
	dt = T/N
	nu = r - q - 0.5 * sigma * sigma
	a = N * (N + 1) * (2 * N + 1) / 6
	V = np.exp(-r*T)*S*np.exp(((N+1)*nu/2 + sigma*sigma*a/(2*N*N))*dt)
	sigavg = sigma * np.sqrt(a) / (N**1.5)
	return black_scholes_euro_call(V, K, r, sigavg, 0, T)

def mc_asian_call_control_variate(S, K, r, sigma, q, T, N, total_simulations):
	dt = T/N
	nudt = (r - q - 0.5 * sigma * sigma) * dt
	sigsdt = sigma * np.sqrt(dt)
	sum_CT = 0
	normal_samples = np.random.normal(size=N)
	for i in range(total_simulations):
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
	portfolio_value = sum_CT / total_simulations * np.exp(-r * T)	
	return portfolio_value + geometric_asian_call(S, K, r, sigma, q, T, N)

if __name__ == "__main__":
	K = 100
	T = 1
	S = 100
	sigma = 0.2
	r = 0.06
	q = 0.03
	N = 10
	total_simulations = 100_000
	print(mc_asian_call_control_variate(S, K, r, sigma, q, T, N, total_simulations))






