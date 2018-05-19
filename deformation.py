import numpy as np

def deform(img, p, q):
    '''Transforming an original image using given control points p and their new points q'''
    # Preconditions:
    #   - img: numpy.array representation of the image with dimension (x, y, 3)
    #   - p: list of tuples representing the control points
    #   - q: list of tuples representing the intended final position of the control points
    # Postcondition:
    #   - ret_img: numpy.array representation of deformed image with dimension (x, y, 3)

    points = create_grid_points(img.shape)
    #transformed_points = [transform(v,p,q) for v in points]
    #ret_img = np.add()

def create_grid_points(img_shape):
    range_x = np.concatenate((np.arange(0, img_shape[0], img_shape[0]/10),
                         np.array([img_shape[0]-1])),
                         axis=0)

    range_y = np.concatenate((np.arange(0, img_shape[1], img_shape[1]/10),
                         np.array([img_shape[1]-1])),
                         axis=0)

    v_points = np.transpose([np.tile(range_x, len(range_y)),
                             np.repeat(range_y, len(range_x))])

    return v_points

def bilinear(img, original, transformed):
    ret_img = np.zeros_like(img)


img = np.reshape(np.arange(1600*3), (-1, 40, 3))
print(type(img.shape))
deform(img, [], [])

arr1 = np.reshape(np.arange(60), (-1, 5, 3))
arr2 = np.reshape(np.arange(0, -60, -1), (-1, 5, 3))
arr3 = np.add(arr1, arr2)
print(arr3)
print(arr3.shape)
