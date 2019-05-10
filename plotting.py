import matplotlib.pyplot as plt
import numpy as np
import calculating
import time
import math

class point_finder:
    def __init__(self, number_of_points=50):
        self.number_of_points_to_create = number_of_points
        self.was_already_perfect = 0
        self.origin_radius = 0
        self.origin_center = [0,0]
        self.origin_longest_distance_points = []
        self.correction_vector = [0,0]
        self.list_of_x_vals = []
        self.list_of_y_vals =[]
        self.list_of_outer_x =[]
        self.list_of_outer_y = []
        self.list_of_outer_points = []
        self.center = []
        self.point_that_changed = None
        self.running_time = 0

        self.random_list_of_points = calculating.generate_random_array(self.number_of_points_to_create)
        self.fill_lists()
        self.starting_point = self.random_list_of_points[self.list_of_y_vals.index(max(self.list_of_y_vals))]

        self.master_function()

    def master_function(self):
        starttime = time.time()
        self.recursive_point_finding() #get the border points
        self.set_first_radius_and_center()
        if self.optimize_circle(): #if something needs to be fixed
            self.fix_radius()
        self.running_time = time.time() -starttime
        print("Time needed for optimization: ",self.running_time)

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

    def get_unit_vector(self,vector):
        return np.array(vector / self.get_length_of_vector(vector))

    def get_length_of_vector(self,vector):
        return math.sqrt((vector[0] ** 2) + (vector[1] ** 2))

    def get_direction_vector(self,point1,point2): #simple vector from points
        return np.array([point1[0]-point2[0],point1[1]-point2[1]])

    def get_original_vector(self,point):
        return self.get_direction_vector(point,self.center)

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

    def set_first_radius_and_center(self):
        self.center = []#[mean(self.list_of_outer_x),mean(self.list_of_outer_y)]
        self.radius = 0
        for points in self.list_of_outer_points:
            for points_2 in self.list_of_outer_points:
                self.vector = np.array([(points_2[0] - points[0]), (points_2[1] - points[1])])
                rad = math.hypot(self.vector[0]/2,self.vector[1]/2)
                if rad > self.radius:
                    self.origin_longest_distance_points = [points,points_2]
                    self.center = np.array(points + 0.5 * self.vector) #set center between furthest points as our first center
                    self.radius = rad
        self.origin_center = self.center
        self.origin_radius = self.radius

    def find_worst_error(self): #returns the point that is furthest of the circle
        worst_error = self.radius
        worst_point = []
        for point in self.list_of_outer_points:
            distance_to_center = self.get_length_of_vector(self.get_original_vector(point))
            if distance_to_center > self.radius and distance_to_center > worst_error:
                worst_error = distance_to_center
                worst_point = point
        return np.array(worst_point),worst_error

    def optimize_circle(self):
        worst_point,worst_point_dist = self.find_worst_error()
        if worst_point_dist == self.radius:
            self.was_already_perfect = 1
            return False
        unit_vec_of_worst_point = self.get_unit_vector(worst_point)
        margin_of_error = worst_point_dist - self.radius
        self.origin_longest_distance_points.append(worst_point)
        self.correction_vector = unit_vec_of_worst_point*margin_of_error
        self.origin_center = self.center
        self.center = self.center + self.correction_vector
        return True

    def fix_radius(self):
        worst_point, worst_point_dist = self.find_worst_error()
        self.origin_radius = self.radius
        self.radius = worst_point_dist

    def get_center_of_three_points(self):
        pass


class plotting:
    def __init__(self):
        self.pointfinder = point_finder()
        self.subplt = plt.subplot()

    def plot_results(self):
        self.subplt.scatter(self.pointfinder.list_of_x_vals, self.pointfinder.list_of_y_vals, s=10, facecolors='none', edgecolors='g')
        self.subplt.scatter(self.pointfinder.list_of_outer_x, self.pointfinder.list_of_outer_y, s=10, facecolors='none', edgecolors='red')
        self.subplt.scatter(self.pointfinder.center[0], self.pointfinder.center[1], s=10, facecolors='none', edgecolors='blue')
        self.subplt.scatter(self.pointfinder.origin_center[0], self.pointfinder.origin_center[1], s=10, facecolors='none', edgecolors='black')
        worst_x = []
        worst_y = []
        for x in self.pointfinder.origin_longest_distance_points:
            worst_x.append(x[0])
            worst_y.append(x[1])

        self.subplt.scatter(worst_x, worst_y, s=10,facecolors='none', edgecolors='orange')

        self.subplt.add_patch(plt.Circle(self.pointfinder.center, self.pointfinder.radius, color='blue', alpha=0.3))
        self.subplt.add_patch(plt.Circle(self.pointfinder.origin_center, self.pointfinder.origin_radius, color='grey', alpha=0.1))
        self.subplt.set_aspect('equal', adjustable='datalim')
        self.subplt.plot()
        plt.show()




