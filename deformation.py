import numpy as np
from scipy.interpolate import interp2d
from transform import transform
import utils

def deform(image, p, q):
    '''Transforming an original image using given control points p and their new points q'''
    # Preconditions:
    #   - image: numpy.array representation of the image with dimension
    #     (x, y, 3)
    #   - p: list of tuples representing the control points
    #   - q: list of tuples representing the intended final position
    #     of the control points
    # Postcondition:
    #   - ret_img: numpy.array representation of deformed image with
    #     dimension (x, y, 3)

    x_step = 20
    y_step = 20
    x_lines = np.array([
        *range(0, image.shape[1] - 1, x_step),
        image.shape[1] - 1])
    y_lines = np.array([
        *range(0, image.shape[0] - 1, y_step),
        image.shape[0] - 1])

    vertices = np.stack(np.meshgrid(x_lines, y_lines), axis=2)

    extra_points = np.array([
        [0, 0], # top left
        [0, image.shape[1] - 1], # top right
        [image.shape[0] - 1, 0], # bottom right
        [image.shape[0] - 1, image.shape[1] - 1], # bottom left corner
        ])

    full_p = np.concatenate([p, extra_points], axis=0)
    full_q = np.concatenate([q, extra_points], axis=0)

    new_vertices = np.array([[transform(v, full_p, full_q) for v in row]
                            for row in vertices])
    # Just in case some of the transformed pixels are transformed out of
    # the dimensions of the original image.
    max_x, max_y = new_vertices.max(axis=1).max(axis=0).astype(np.int)
    new_image = np.tile(utils.colors['red'], (max_x + 1, max_y + 1, 1))

    for i in range(new_vertices.shape[0] - 1):
        for j in range(new_vertices.shape[1] - 1):
            # The order of the vertices is important. The rows of
            # new_quad must specify the edges of a quadrilateral. So,
            # for all rows, new_quad[l - 1], new_quad[l] are an edge
            # in a quadrilateral, where l is just some index.
            new_quad = np.array([
                new_vertices[i, j],
                new_vertices[i + 1, j],
                new_vertices[i + 1, j + 1],
                new_vertices[i, j + 1],
                ])
            old_quad = np.array([
                vertices[i, j],
                vertices[i + 1, j],
                vertices[i + 1, j + 1],
                vertices[i, j + 1],
                ])
            points = utils.enumerate_points_in_polygon(new_quad)
            points_x, points_y = points[:, 0], points[:, 1]
            inside_picture = (
                    (points_x >= 0) &
                    (points_x < new_image.shape[1]) &
                    (points_y >= 0) &
                    (points_y < new_image.shape[0]))
            points = points[inside_picture]
            # it's possible for all the pixels in new_quad to lie
            # outside the image.
            if (points.shape[0] == 0):
                continue
            new_x_coords, new_y_coords = new_quad[:, 0], new_quad[:, 1]
            old_x_coords, old_y_coords = old_quad[:, 0], old_quad[:, 1]
            interpx = interp2d(new_x_coords, new_y_coords, old_x_coords)
            interpy = interp2d(new_x_coords, new_y_coords, old_y_coords)
            estimated_old_points = np.array([
                np.squeeze([interpx(x, y), interpy(x, y)]) for x, y in points
                ])
            nearest_old_pixels = np.around(estimated_old_points).astype(np.int)
            print("Shape of nearest_old_pixels",
                    nearest_old_pixels.shape)
            print("new quad:",
                    new_quad)
            print("shape of points:", points.shape)
            near_x, near_y = nearest_old_pixels[:, 0], nearest_old_pixels[:, 1]
            in_bounds = (
                    (near_x < image.shape[1]) & 
                    (near_x >= 0) &
                    (near_y < image.shape[0]) & 
                    (near_y >= 0))
            old_colors = np.empty((nearest_old_pixels.shape[0], 3))
            """
            print("Shape of in_bounds", in_bounds.shape)
            print("Shape of old colors", old_colors.shape)
            print("Shape of old_colors[in_bounds]",
                    old_colors[in_bounds].shape)
            print("Shape of nearest_old_pixels",
                    nearest_old_pixels.shape)
            print("Shape of nearest_old_pixels[in_bounds]",
                    nearest_old_pixels[in_bounds].shape)
            print("Shape of index arrays:", 
                  [A.ravel().shape
                   for A in np.split(
                       nearest_old_pixels[in_bounds], 2, axis=1)])
            print("Shape of image[nearest_old_pixels_idx]",
                  image[[A.ravel()
                   for A in np.split(
                       nearest_old_pixels[in_bounds], 2, axis=1)]].shape)
            print("Shape of new_image", new_image.shape)
            print("Shape of new_image[split points]",
                  new_image[np.split(points, 2, axis=1)[::-1]].shape)
            print("Shape of new_image[points_idx]",
                  new_image[[
                    A.ravel() for A in np.split(
                        points, 2, axis=1)][::-1]].shape)
            """
            # This is the basic idea, but some of the
            # nearest_old_pixels can be outside of the old image's
            # dimensions.
            # old_colors = image[np.split(nearest_old_pixels, 2, axis=1)[::-1]]
            # new_image[np.split(points, 2, axis=1)[::-1]] = old_colors
            valid_x, valid_y = [A.ravel() for A in np.split(nearest_old_pixels[in_bounds], 2, axis=1)]
            #print(image[valid_y, valid_x].shape)
            old_colors[in_bounds] = image[valid_y, valid_x]
            #print(old_colors.shape)

            """
            old_colors[in_bounds] = image[[A.ravel() 
                for A in np.split(
                    nearest_old_pixels[in_bounds], 2, axis=1)][::-1]]
            """
            old_colors[~in_bounds] = utils.colors['red']
            new_image[[A.ravel() for A in np.split(points, 2, axis=1)][::-1]] = old_colors

    return new_image

def create_grid_points(img_shape):
    # The x lines of the grid. Includes the start (left), there's 10
    # (ish?) ticks total, and the final element is always the right
    # edge of the picture.
    range_x = np.concatenate((np.arange(0, img_shape[0], img_shape[0]/10),
                         np.array([img_shape[0]-1])),
                         axis=0)

    # The y lines of the grid. Includes the start (top), there's 10
    # (ish?) ticks total, and the final element is always the bottom
    # end of the picture.
    range_y = np.concatenate((np.arange(0, img_shape[1], img_shape[1]/10),
                         np.array([img_shape[1]-1])),
                         axis=0)

    v_points = np.transpose([np.tile(range_x, len(range_y)),
                             np.repeat(range_y, len(range_x))])

    # This function is equivalent to:
    #   np.stack(np.meshgrid(range_x, range_y), axis=2)
    # The idea is to just return an array containing the cartesian
    # products of desired x points and y points on the grid.
    return np.reshape(v_points, (range_x.shape[0], range_y.shape[0], 2))

def get_transformed_box(img, original, transformed):
    '''Takes section of image bounded by coordinates in original and returns an array of the same shape as image with the corresponding values in the transformed section being the interpolated value'''
    # Preconditions:
    #   - img: numpy.array representation of the image with dimension (x, y, 3)
    #   - original: numpy.array representation of the corners of the current box to operate in. These always have dimension (2, 2, 2). There's four corners (the first (2,2), and each corner is a 2D coordinate, thus the 3rd dimension of the array is 2.  
    #   - transformed: numpy.array representation of the corners of the transformation of the original corners.

    top_left = original[0,0]
    bottom_left = original[0,1]
    top_right = original[1,0]
    bottom_right = original[1,1]

    left = top_left[0]
    right = top_right[0]
    top = top_left[1]
    bottom = bottom_left[1]

    trans_top_left = transformed[0,0]
    trans_bottom_left = transformed[0,1]
    trans_top_right = transformed[1,0]
    trans_bottom_right = transformed[1,1]

    original_box = [[x,y] 
                    for x in range(left, right+1)
                    for y in range(top, bottom+1)]


    # Get list of points within the box. Include the corners for now.


    ret_img = np.zeros_like(img)

    #TODO:
    # - Normalize box bounded by original to be 0 to 1 in both directions
    # - Interpolate using scipy on that box using the values from the original image
    # - Create a mapping from the normalized (0 to 1) original box to the trasformed box (quadralateral) bounded by transformed
    # - Calculate the interpolated value of the integer coordinates inside the transformed box using the mapping to the original box and the interpolation on the original box
    # - return an array of the same dimensions as the original image with only the values of the integer coordinate points inside the transformed box being nonzero

    return ret_img
