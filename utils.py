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

def to_rgb_image(image):
    # Preconditions:
    # - image is a 2D image
    # Postconditions:
    # - Returns a 3D array representing a 2D image with 3 color
    #   channels. The output can be placed directly in plt.plot() to
    #   display a picture.
    return np.tile(np.expand_dims(image, 2), (1,1,3))

def rotate_corners(left, top, right, bottom, degrees):
    # Preconditions:
    # - left, top, right, bottom : These are floats indicated the
    #   left, top, right, and bottom of a rectangle.
    # - degrees : A float specifying the number of degrees to rotate
    #   the rectangle counterclockwise about the origin.
    theta = degrees * (np.pi / 180)
    rotation = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)],
        ])
    midpoint = np.array([left + right, top + bottom])/2
    new = np.array([
        rotation.dot([left, top] - midpoint) + midpoint,
        rotation.dot([right, top] - midpoint) + midpoint,
        rotation.dot([left, bottom] - midpoint) + midpoint,
        rotation.dot([right, bottom] - midpoint) + midpoint,
    ])
    return new

