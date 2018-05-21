import numpy as np
from matplotlib import pyplot as plt

def normalize(x, minimum, maximum):
    return (x - minimum) / (maximum - minimum)

# TODO:
# - Make simpler transforms: a translation, a rotation, scale up,
#   scale down. See if those work as expected.

# - Do I need the original and the new corners of the boxes?
# - This interpolation is a function that returns a tuple of
#   coordinates. We're going from coordinates to coordinates.
# - Take in the original corners for normalization of the input.
# - Use the new corners to create the interpolation.

class bilinear:
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

def rotate_corners(left, top, right, bottom, degrees):
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

# Create original image
image = np.full((50, 50), 255)
width = 11
height = 11
top_left = [10, 20]
top = top_left[1]
left = top_left[0]
right = left + width - 1
bottom = top + height - 1
width_slice = slice(left, left + width)
height_slice = slice(top, top + height)

# NOTE: numpy array has indices of the form (rows, columns). For an
# image, this translates into (vertical, horizontal).

# Fill in selected region with random colors.
image[height_slice, width_slice] = np.random.randint(
        200, 250, (width, height))

# Get the corners of the region.
original = np.stack(np.meshgrid([left, right], [top, bottom]), axis=2)
# Index matrices for the original corners.
original_idx = np.meshgrid([left, right], [top, bottom])

# Get the points within and on the boundaries of the region.
points = np.meshgrid(
        np.arange(left, left + width), np.arange(top, top + height))
#points = original_idx

# Color the corners black.
image[[A.ravel() for A in original_idx][::-1]] = 0

# Pick the transformations for the corners.
#new = np.array([[[10, 20], [15, 20]], [[12, 30], [15, 30]]])
"""
new = np.array([
    [[left + 10, top], [right + 10, top]],
    [[left + 10, bottom], [right + 10, bottom]]])
"""
"""
angle = 45
new = rotate_corners(left, top, right, bottom, angle).astype(np.int).reshape((2,2,2))
"""
new = np.array([
    [left * 2, top],
    [])]
#new = (original - top_left) * 2 + top_left
print(new.shape)
transform = bilinear(original, new)

print("original points:", original)
print("new points:", new)

# Reshape points into an array of coordinates.
transformations = np.array([transform(x, y) 
                   for x, y in
                   np.stack(points, axis=2).reshape(-1, 2)])
np.round(transformations)
transformations = transformations.astype(np.int)
#new_points = np.split(transformations, 2, axis=1)
#print("Transformations:\n", transformations)

new_image = np.full_like(image, 255)
for old, new in zip(np.stack(points, axis=2).reshape(-1, 2),
                    transformations):
    print(old, new)
    #print(image[old])
    #print(new_image[new])
    new_image[new[1], new[0]] = image[old[1], old[0]]

fig, axes = plt.subplots(nrows=1, ncols=2)
colormap = None
axes[0].imshow(
        np.tile(
            np.expand_dims(image, 2), (1,1,3)),
        interpolation='nearest')
axes[0].set_title("Original image")
axes[1].imshow(
        np.tile(
            np.expand_dims(new_image, 2), (1,1,3)),
        interpolation='nearest')
axes[1].set_title("Transformed image")
fig.suptitle("New Corners as dilation of old corners")
plt.show()

