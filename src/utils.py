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

def cartesian_product_points(x_points, y_points):
    # Preconditions:
    # - x_points, y_points are 1D numpy arrays that represent a set of
    #   x coordinates and y coordinates respectively. For instance,
    #   x_points = [0, 1], y_points = [2, 3]. This should result in
    #   the set of all points [[0, 2], [0, 3], [1, 2], [1, 3]].
    # Postconditions:
    # - Returns a 2D numpy array of shape (points_in_box, 2) such that
    #   each row is a point whose x coordinate was in x_points and y
    #   coordinate was in y_points.
    grid = np.meshgrid(x_points, y_points)
    return [A.ravel() for A in grid]

# Source: <https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html>
def point_in_polygon(point, corners):
    # Preconditions:
    # - corners is a 2D numpy array of shape (numCorners, 2). Each
    #   row should be an (x, y) coordinate in 2D space such that
    #   corners[i-1], corners[i] forms an edge of the polygon.
    numCorners = corners.shape[0]
    min_x, min_y = corners.min(axis=0)
    max_x, max_y = corners.max(axis=0)
    if (any([point[0] < min_x, point[0] > max_x, point[1] < min_y,
             point[1] > max_y])):
        return False
    inside = False
    for i in range(numCorners):
        start = corners[i - 1]
        end = corners[i]
        if (((end[1] > point[1]) != (start[1] > point[1])) and
            (point[0] < 
                ((start[0] - end[0]) * 
                    (point[1] - end[1]) / 
                    (start[1] - end[1]) + end[0]))):
            inside = not inside
    return inside

def enumerate_points_in_polygon(corners):
    # Preconditions:
    # - corners is a 2D numpy array of shape (num_corners, 2). Each
    #   row should be an (x, y) coordinate in 2D space such that
    #   corners[i-1], corners[i] forms an edge of the polygon.
    # Postconditions:
    # - Returns a 2D numpy array of shape (points_found, 2), where
    #   each row is a pixel location that is inside of the specified
    #   polygon.
    min_x, min_y = corners.min(axis=0)
    max_x, max_y = corners.max(axis=0)
    points = np.stack(
            cartesian_product_points(
                np.arange(min_x, max_x + 1),
                np.arange(min_y, max_y + 1)),
            axis=1).astype(np.int)
    return np.array([p for p in points if point_in_polygon(p, corners)])



colors = {
    'red' : [0xa9, 0x3f, 0x55],
    'white' : [255, 255, 255],
}
