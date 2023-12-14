from black_scholes import black_scholes_euro_call
from mc_euro_call_no_slurm import mc_euro_call

strike_prices = [90,100]
sim_accurate = [0,0,0,0,0]     
K = 100      
r = 0.05     
sigma = 0.2
q = 0.02
T = 5    
target_accuracy = .01  # Desired level of accuracy 
min_simulations = 50_000_000  # Minimum number of simulations to start with
step_size = 10000  # Number of simulations to increase in each iteration

current_simulations = min_simulations

while sim_accurate.__contains__(False):
    current_simulations += step_size
    for S in range(len(strike_prices)):
        sim_accurate[S] = abs(mc_euro_call(strike_prices[S], K, r, sigma, q, T, current_simulations) - black_scholes_euro_call(strike_prices[S],K,r,sigma,q,T)) < target_accuracy


print(f"Simulations: {current_simulations}")
print(f"Accuracy: {mc_euro_call(strike_prices[S], K, r, sigma, q, T, current_simulations) - black_scholes_euro_call(strike_prices[S],K,r,sigma,q,T)}")
print(sim_accurate)