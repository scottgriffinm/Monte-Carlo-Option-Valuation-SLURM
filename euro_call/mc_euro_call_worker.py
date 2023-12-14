import numpy as np
import sys

def mc_euro_call_worker(S, K, r, sigma, q, T, n, M):
    drift = (r - q - 0.5 * sigma**2) * T
    sig_sqrt_t = sigma * np.sqrt(T)
    up_change = np.log(1.01)
    down_change = np.log(0.99)
    sum_call = 0
    sum_call_change = 0
    sum_pathwise = 0
    random_numbers = np.random.randn(M)
    for i in range(n):
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
    return sum_call/M

if __name__ == "__main__":
    S = float(sys.argv[1])
    K = float(sys.argv[2])
    r = float(sys.argv[3])
    sigma = float(sys.argv[4])
    q = float(sys.argv[5])
    T = int(sys.argv[6])
    n = int(sys.argv[7])
    M = int(sys.argv[8])
    print(mc_euro_call_worker(S, K, r, sigma, q, T, n, M))




