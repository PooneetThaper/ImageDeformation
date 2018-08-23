def normalize(x, minimum, maximum):
    return (x - minimum) / (maximum - minimum)

class bilinear:
    """
    An object of this class performs bilinear interpolation. It takes
    the points the interpolate and performs all of the normalization
    internally.

    Parameters
    ==========
    original_corners : numpy.ndarray
        The four points with which to create the linear
        interpolations. This is expected to be a rectangle in a 2D
        plane. Dimensions are (2, 2, 2), such that:
        - original_corners[0, 0] is top left corner
        - original_corners[0,1] is the top_right corner
        - original_corners[1,0] is the bottom_left corner
        - original_corners[1,1] is the bottom_right corner
    new_corners : numpy.ndarray
        These are the new corners that the original corners map onto.
        The structure is similar to original_corners argument. A
        (2,2,2) array such that:
        - new_corners[0, 0] is the new top left corner
        - new_corners[0,1] is the new top_right corner
        - new_corners[1,0] is the new bottom_left corner
        - new_corners[1,1] is the new bottom_right corner
    """

    def __init__(self, original_corners, new_corners):
        top_left = original_corners[0,0]
        top_right = original_corners[0,1]
        bottom_left = original_corners[1,0]
        bottom_right = original_corners[1,1]

        # the original_idx should create a rectangle.
        self.left = top_left[0]
        self.right = top_right[0]
        self.top = top_left[1]
        self.bottom = bottom_left[1]

        # These are the function values to interpolate, which are
        # vectors (coordinates), rather than scalars.
        # They don't have to be the top left/top right/... of a box,
        # but, in general, transform(top, left) = self.top_left,
        # transform(top, right) = self.top_right.
        self.top_left = new_corners[0,0]
        self.top_right = new_corners[0,1]
        self.bottom_left = new_corners[1,0]
        self.bottom_right = new_corners[1,1]

    def normalize(self, point):
        x, y = point[0], point[1]
        return (normalize(x, self.left, self.right), 
                normalize(y, self.top, self.bottom))

    def interpolate_point(self, x, y):
        normX, normY = self.normalize((x,y))
        return (
            (1 - normX) * (1 - normY) * self.top_left + 
            normX * (1 - normY) * self.top_right + 
            (1 - normX) * normY * self.bottom_left +
            normX * normY * self.bottom_right
        )

    def __call__(self, x, y):
        return self.interpolate_point(x, y)
