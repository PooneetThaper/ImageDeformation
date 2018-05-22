import numpy as np

def pointInArray(p, arr):
    # Preconditions:
    # - p is a 1D numpy arroy of 2 coordinates.
    # - arr is a 2D numpy array, such that each row is a point with 2
    #   coordinates. Thus the shape should be (*, 2), where "*" is
    #   some integer.
    # Postconditions:
    # - returns True if p is equal to one of the rows in arr. Returns
    #   false otherwise.
    equal_mask = (np.tile(p, (arr.shape[0], 1)) == arr)
    point_equal_mask = equal_mask.sum(axis=1) == 2
    return point_equal_mask.sum().astype(np.bool)

def pointLocationInArray(p, arr):
    # Preconditions:
    # - p is a 1D numpy arroy of 2 coordinates.
    # - arr is a 2D numpy array, such that each row is a point with 2
    #   coordinates. Thus the shape should be (*, 2), where "*" is
    #   some integer.
    # Postconditions:
    # - returns index, i,  of arr such that arr[i] == p, if such an i
    #   exists. Returns -1 otherwise.
    equal_mask = (np.tile(p, (arr.shape[0], 1)) == arr)
    point_equal_mask = equal_mask.sum(axis=1) == 2
    # np.where returns a tuple which contains an array.
    location = np.where(point_equal_mask)[0]
    return (location[0]
            if location.size != 0
            else -1)

def get_weight(p, v, a): #p, v are row vectors [x y]
        # - p, v : 1D numpy arrays. Represent locations in an image.
        # - a : Float, the alpha parameter from the paper.
	array_subtract = np.array(np.subtract(p,v))
	square_second_norm = (array_subtract[0]**2 + array_subtract[1]**2)**a
	return 1/square_second_norm #returns individual weight, Wi

def get_weighted_centroids(x, w):
        # Preconditions:
        # - x : 2D numpy array, where each row is a point. These
        #   points are either the p (original locations of handles) or
        #   q (the final location of handles).
        # - w : 1D numpy array, where each element is a weight. These
        #   weights are produced by get_weight, so they are specific
        #   to a point in the image.
        # - x and w should have the same amount of rows. In other
        #   words, x.shape[0] == w.size
        # Postconditions:
        # - returns a single centroid as a 1D numpy array.
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
        # Preconditions:
        # - phat_arr : a 2D numpy array where each row is the
        #   difference between the original location of a handle and
        #   the weighted centroid of the handles.
        # - qhat_arr : A 2D numpy array similar to phat_arr, but using
        #   the final locations of handles instead of the original
        #   location.
        # - w_arr : A 1D numpy array of weights.
        # - number of points in p, points in q, and weights in w_arr
        #   should all be the same.
        #   phat_arr.shape[0] == qhat_arr.shape[0] == w_arr.shape[0]
        # Postconditions:
        # - Returns M, the 2x2 transformation matrix for the point v.
        #   v is not an argument to this function, but the weights in
        #   w_arr were calculated relative to this point.
	i = len(phat_arr)
	j = len(phat_arr)
	sigma1 = np.zeros((phat_arr.shape[1], qhat_arr.shape[1]))
	sigma2 = np.zeros((phat_arr.shape[1], qhat_arr.shape[1]))
	for temp in range(i):
                phat_i = phat_arr[temp]
                # Proper matrix computations require np.dot. Since we
                # are multiplying two row vectors to do it, np.outer
                # suffices. np.outer(u, v) = u^T * v, where * is
                # matrix multiplication.
                sigma1 += np.outer(phat_i, w_arr[temp] * phat_i)
	sigma1_inv = np.linalg.inv(sigma1)
	for temp in range(j):
		sigma2 += w_arr[temp] * np.outer(phat_arr[temp], qhat_arr[temp])
	return sigma1_inv.dot(sigma2)

def deformation(x, pstar, M, qstar):
	return (x-pstar).dot(M) + qstar

def transform(v, p, q, a=2):
        # Preconditions:
        # - p : a 2D numpy array of the original locations of the
        #   handles. Each row is a location.
        # - q : a 2D numpy array of the final locations of the
        #   handles. Each row is a location.
        # - v : a 1D numpy array representing the current point to
        #   deform.
        # - a, optional : a float parameter which tunes the values of
        #   the weights.
        # Postconditions:
        # - The return value is the moving least squares deformation
        #   of the point v with p as the original position of handles
        #   and q as the new position of handles.
        location = pointLocationInArray(v, p)
        if location != -1:
            return q[location]
        w_arr = [get_weight(handle, v, a)
                 for handle in p]
        p_centroid = get_weighted_centroids(p, w_arr)
        q_centroid = get_weighted_centroids(q, w_arr)
        phat_arr = np.array([get_pq_hat(handle, p_centroid)
                             for handle in p])
        qhat_arr = np.array([get_pq_hat(handle, q_centroid)
                             for handle in q])
        M = least_square(phat_arr, qhat_arr, w_arr)
        return deformation(v, p_centroid, M, q_centroid)
