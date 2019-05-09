import matplotlib.pyplot as plt
import numpy as np
import calculating
import numpy.linalg as la
from statistics import mean
import math

class point_finder:
    def __init__(self, number_of_points=50):
        self.random_list_of_points = calculating.generate_random_array(number_of_points)
        self.list_of_x_vals = []
        self.list_of_y_vals =[]
        self.list_of_outer_x =[]
        self.list_of_outer_y = []
        self.list_of_outer_points = []
        self.middle_point = []
        self.fill_lists()
        self.starting_point = self.random_list_of_points[self.list_of_y_vals.index(max(self.list_of_y_vals))]

    def fill_lists(self):
        for x in self.random_list_of_points:
            self.list_of_x_vals.append(x[0])
            self.list_of_y_vals.append(x[1])

    def get_quadrant(self,point):  # get the quadrant the point is in
        if point[0] > 0:  # if the x-coord is bigger than 0 ...
            if point[1] > 0:  # and the y-coord is too, then return
                return 1  # first quadrant
            else:
                return 4  # fourth quadrant
        else:
            if point[1] > 0:
                return 2  # second quadrant
            else:
                return 3  # third quadrant

    def get_angle_between_vectors(self,v1, v2):
        """ Returns the angle in degrees between vectors 'v1' and 'v2'    """
        angle = np.math.atan2(np.linalg.det([v1, v2]), np.dot(v1, v2))
        return np.degrees(angle)

    def test_neighbour_points(self,point):
        """this function should return all the outer points. We get the most up point and then test all
        the points to the right. We will build the vector between the two testing points and then get the
        angle of the resulting vector against one of the axes(dependent on the quadrant the point is in).
        The point with the smallest angle has to be the next outer point. This function will recursively
        call itself until it finds itself on its starting-point. The resulting point are saved in a list"""

        quadrant_this_point_is_in = self.get_quadrant(point)
        vector_to_test_against = []

        if quadrant_this_point_is_in is 1:
            vector_to_test_against = [1, 1]
        elif quadrant_this_point_is_in is 2:
            vector_to_test_against = [-1, 1]
        elif quadrant_this_point_is_in is 3:
            vector_to_test_against = [-1, -1]
        elif quadrant_this_point_is_in is 4:
            vector_to_test_against = [1, -1]

        neighbour_point=[]
        smallest_angle = 0
        for idx, val in enumerate(self.random_list_of_points):
            if val is point:
                pass #dont test against the own point
            else:
                vector_between_the_two_points = np.array([point[0] - val[0], point[1] - val[1]])
                angle = self.get_angle_between_vectors(vector_to_test_against, vector_between_the_two_points)
                if angle < smallest_angle:
                    neighbour_point = val
                    smallest_angle = angle
        return neighbour_point

    def recursive_point_finding(self):
        point_to_test = self.starting_point

        while point_to_test not in self.list_of_outer_points:
            self.list_of_outer_points.append(point_to_test)
            point_to_test = self.test_neighbour_points(point_to_test)

        for x in self.list_of_outer_points:
            self.list_of_outer_x.append(x[0])
            self.list_of_outer_y.append(x[1])

    def get_longest_distance_between_outer_points(self):
        self.middle_point = []#[mean(self.list_of_outer_x),mean(self.list_of_outer_y)]
        self.longest_dist = 0
        for points in self.list_of_outer_points:
            for points_2 in self.list_of_outer_points:
                self.vector = [(points_2[0] - points[0]), (points_2[1] - points[1])]
                dist = math.hypot(self.vector[0]/2,self.vector[1]/2)
                if dist > self.longest_dist:
                    self.middle_point = [0,0]
                    self.longest_dist = dist


x = point_finder()
x.recursive_point_finding()
x.get_longest_distance_between_outer_points()
radius  = x.longest_dist


subplt = plt.subplot()
print(x.longest_dist)
plt.scatter(x.list_of_x_vals, x.list_of_y_vals, s=10, facecolors='none', edgecolors='g')
plt.scatter(x.list_of_outer_x,x.list_of_outer_y, s=10, facecolors='none', edgecolors='red')
subplt.add_patch(plt.Circle(x.middle_point, radius, color='purple', alpha=0.3))
subplt.set_aspect('equal', adjustable='datalim')
subplt.plot()
plt.show()