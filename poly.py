from matplotlib.path import Path
import numpy as np

def poly_from_points(vertices):
    ''' Takes as input the points outlining a polygon and returns a matplotlib.path.Path object'''
    # To find out if a point is in that polygon, do [returned polygon].contains_point(test_point)
    vertices = np.append(vertices, [vertices[0]], axis=0)
    print(vertices.shape)
    print(vertices)
    codes = [Path.MOVETO] + ([Path.LINETO]*(vertices.shape[0]-2)) + [Path.CLOSEPOLY]
    return Path(vertices, codes, closed=True)


if __name__ == "__main__":
    # Testing:
    poly_points = np.array([[0,-1], [-1,0], [0,1], [1,0]])
    path = poly_from_points(poly_points)

    test_points = np.array([[0.5,0], [1,1]])
    for test_point in test_points:
        print(path.contains_point(test_point))
    # Should be True then False

    # Plot the results
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig = plt.figure()
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor='none', lw=1)
    ax.add_patch(patch)
    ax.scatter(test_points[:,0], test_points[:,1])
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    plt.show()
