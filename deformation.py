import numpy as np
from scipy import interpolate

def deform(img, p, q):
    '''Transforming an original image using given control points p and their new points q'''
    # Preconditions:
    #   - img: numpy.array representation of the image with dimension (x, y, 3)
    #   - p: list of tuples representing the control points
    #   - q: list of tuples representing the intended final position of the control points
    # Postcondition:
    #   - ret_img: numpy.array representation of deformed image with dimension (x, y, 3)

    points = create_grid_points(img.shape)
    transformed_points = np.array([[transform(v,p,q) for v in row] for row in grid])

    ret_img = np.zeros_like(img)
    for i in range(points.shape[0]-1):
        for j in range(points.shape[1]-1):
            transformed_box = get_transformed_box(img, points[i:i+2][j:j+2],
                                                       transformed_points[i:i+2][j:j+2])
            np.copyto(ret_img, transformed_box,
                      np.where(transformed_box > 0, 1,0))
    return ret_img

def create_grid_points(img_shape):
    range_x = np.concatenate((np.arange(0, img_shape[0], img_shape[0]/10),
                         np.array([img_shape[0]-1])),
                         axis=0)

    range_y = np.concatenate((np.arange(0, img_shape[1], img_shape[1]/10),
                         np.array([img_shape[1]-1])),
                         axis=0)

    v_points = np.transpose([np.tile(range_x, len(range_y)),
                             np.repeat(range_y, len(range_x))])

    return np.reshape(v_points, (range_x.shape[0], range_y.shape[0], 2))

def get_transformed_box(img, original, transformed):
    '''Takes section of image bounded by coordinates in original and returns an array of the same shape as image with the corresponding values in the transformed section being the interpolated value'''

    ret_img = np.zeros_like(img)

    #TODO:
    # - Normalize box bounded by original to be 0 to 1 in both directions
    # - Interpolate using scipy on that box using the values from the original image
    # - Create a mapping from the normalized (0 to 1) original box to the trasformed box (quadralateral) bounded by transformed
    # - Calculate the interpolated value of the integer coordinates inside the transformed box using the mapping to the original box and the interpolation on the original box
    # - return an array of the same dimensions as the original image with only the values of the integer coordinate points inside the transformed box being nonzero

    return ret_img

img = np.reshape(np.arange(1600*3), (-1, 40, 3))
print(img.shape)
deform(img, [], [])
