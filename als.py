import numpy as np
from numpy.linalg import lstsq


def als(A, k, num_iter, init_W = None, init_H = None, print_enabled = False):
	'''
	Run the alternating least squares method to perform nonnegative matrix factorization on A.
	Return matrices W, H such that A = WH.
	
	Parameters:
		A: ndarray
			- m by n matrix to factorize
		k: int
			- integer specifying the column length of W / the row length of H
			- the resulting matrices W, H will have sizes of m by k and k by n, respectively
		num_iter: int
			- number of iterations for the multiplicative updates algorithm
		print_enabled: boolean
			- if ture, output print statements

	Returns:
		W: ndarray
			- m by k matrix where k = dim
		H: ndarray
			- k by n matrix where k = dim
	'''

	print('Applying the alternating least squares method on the input matrix...')

	if print_enabled:
		print('---------------------------------------------------------------------')
		print('Frobenius norm ||A - WH||_F')
		print('')

	# Initialize W and H
	if init_W is None:
		W = np.random.rand(np.size(A, 0), k)
	else:
		W = init_W

	if init_H is None:
		H = np.random.rand(k, np.size(A, 1))
	else:
		H = init_H

	# Decompose the input matrix
	for n in range(num_iter):
		# Update H
		# Solve the least squares problem: argmin_H ||WH - A||
		H = lstsq(W, A, rcond = -1)[0]
		# Set negative elements of H to 0
		H[H < 0] = 0

	    # Update W
		# Solve the least squares problem: argmin_W.T ||H.TW.T - A.T||
		W = lstsq(H.T, A.T, rcond = -1)[0].T

		# Set negative elements of W to 0
		W[W < 0] = 0

		if print_enabled:
			frob_norm = np.linalg.norm(A - W @ H, 'fro')
			print("iteration " + str(n + 1) + ": " + str(frob_norm))

	return W, H