from utils import *
from q4 import *

theta = degrees_to_radians(60.0)
theta_prime = diminished_angle(theta)

depths = get_depths(4, 2, 110, degrees_to_radians(1.5))
depths = depth_to_numpy(depths)
depths = depths.T
# depths = interpolate(depths, 4)
guide_ab = (-1, 0)



if __name__ == '__main__':
    train(depths, guide_ab, 5)