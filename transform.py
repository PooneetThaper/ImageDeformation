import numpy as np

def get_weight(p, v, a): #p, v are row vectors [x y]
	array_subtract = np.array(np.subtract(p,v))
	square_second_norm = (tuple_subtract[0]**2 + tuple_subtract[1]**2)**a
	return 1/square_second_norm #returns individual weight, Wi

def get_weighted_centroids(x, w): #x is all set of points (p or q), w is all calculated weights
	sigmaWiPi = 0
	sigmaWi = 0
	n = len(x)
	for i in range(n):
		sigmaWiPi += (x[i]*w[i]) 
		sigmaWi += w[i]
	return sigmaWiPi/sigmaWi #returns p/q star, a numpy array of length 2

def get_pq_hat(xi, xstar): #x is either pi/qi or pstar/qstar
	return np.array(np.subtract(xi,xstar)) #returns p/q hat

def least_square(phat_arr, qhat_arr, w_arr):
	i = len(phat_arr)
	j = len(phat_arr)
	sigma1 = 0
	sigma2 = 0
	for temp in range(i):
		phat_i = phat_arr[temp]
		phat_i_transpose = np.tranpose(phat_i)
		sigma1 += phat_i_tranpose * w_arr[temp] * phat_i
	sigma1_inv = np.linalg.inv(sigma1)
	for temp in range(j):
		phat_j_transpose = np.transpose(phat_arr[temp])
		sigma2 += w_arr[temp] * phat_j_transpose * qhat_arr[temp]
	return sigma1_inv * sigma2

def deformation(x, pstar, M, qstar):
	return (x-pstar)*M + qstar