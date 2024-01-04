from time import time
import numpy as np
from statistics import mean

def mc_euro_call(S, K, r, sigma, q, T, M):
	'''
	Computes the price of a European call option using Monte Carlo simulation.

	S: float, initial stock price
	K: float, strike price
	r: float, risk-free rate
	sigma: float, volatility
	q: float, dividend yield
	T: int, time to maturity in years
	M: int, number of simulations
	'''
	sum_call = 0
	drift = (r - q - 0.5 * sigma**2) * T
	sig_sqrt_t = sigma * np.sqrt(T)
	up_change = np.log(1.01)
	down_change = np.log(0.99)
	sum_call = 0
	sum_call_change = 0
	sum_pathwise = 0
	random_numbers = np.random.randn(M) # Precompute random numbers
	for i in range(M): # Simulate M asset paths
		log_st = np.log(S) + drift + sig_sqrt_t * random_numbers[i]
		call_val = max(0, np.exp(log_st) - K)
		sum_call += call_val
		log_su = log_st + up_change
		call_vu = max(0, np.exp(log_su) - K)
		log_sd = log_st + down_change
		call_vd = max(0, np.exp(log_sd) - K)
		sum_call_change += call_vu - call_vd
		if np.exp(log_st) > K:
			sum_pathwise += (np.exp(log_st) / S)
	# Discount average call value to present time	
	call_value = np.exp(-r * T) * sum_call/M 
	return call_value


if __name__ == "__main__":
	# Option parameters
	S = 110   
	K = 100      
	r = 0.05     
	sigma = 0.2 
	q = 0.01       
	T = 1

	# Average runtime and average price error experiment
	M = 100000000 # Number of simulations
	bs_price = 16.79983686 # Black-Scholes price to compare to
	runs = 10 # Number of runs to average over
	average_runtime = 0
	runtimes = []
	prices = []
	for i in range(runs):
		print(f"\nrun {i}/{runs}")
		start = time()	
		price = mc_euro_call(S, K, r, sigma, q, T, M)
		end = time()
		runtime = end-start
		runtimes.append(runtime)
		prices.append(price)
		average_runtime += runtime/runs		
		print(f"sims = {M}")
		print(f"price = {price}")
		print(f"time = {round(runtime,6)} seconds")
		print(f"running_average = {round((average_runtime*runs)/(i+1),6)}")

	# Calculate and print results
	average_runtime = round(mean(runtimes),5)
	average_error = float(round(abs(mean(prices)-bs_price),5))
	print("---------------------------------------------------")
	print(f"\nsingle, independent computer")
	print(f"sims = {M}")
	print(f"\nRUNTIMES")
	for i in range(len(runtimes)):
		print(f"run {i}, {runtimes[i]} seconds.")
	print(f"\nPRICES")
	for i in range(len(prices)):
		print(f"run {i}, {prices[i]}")
	print(f"\nAVERAGE RUNTIME = {average_runtime}")
	print(f"AVERAGE ERROR = {average_error}")
	
	
	


