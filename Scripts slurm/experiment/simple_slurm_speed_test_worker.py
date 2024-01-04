import numpy as np
import sys

'''Worker computer script for calculating the average of a number of random numbers.'''

if __name__ == "__main__":
	iters = int(sys.argv[1])
	random_avg = 0
	for i in range(iters):
		random_avg += np.random.randn()/iters 
	print(random_avg)
