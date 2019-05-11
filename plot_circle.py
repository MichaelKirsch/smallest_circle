import matplotlib.pyplot as plt
import random
import numpy as np
import time
import math

class point_finder: #find the smallest radius around a set of points
    def __init__(self, number_of_points):
        self.number_of_points_to_create = number_of_points
        self.was_already_perfect = 0
        self.origin_radius = 0
        self.origin_center = [0,0]
        self.correction_vector = [0,0]
        self.list_of_x_vals = []
        self.list_of_y_vals =[]
        self.list_of_outer_x =[]
        self.list_of_outer_y = []
        self.list_of_outer_points = []
        self.center = []
        self.radius = 0
        self.point_that_changed = None
        self.running_time = 0

        self.random_list_of_points = self.generate_random_array(number_of_points)
        self.fill_lists()
        self.starting_point = self.random_list_of_points[self.list_of_y_vals.index(max(self.list_of_y_vals))]

        self.master_function()

    def master_function(self): #this functions calls all the other clas functions. its just here to keep track more easy
        starttime = time.time()
        self.recursive_point_finding() #get the border points
        self.set_first_radius_and_center()
        if self.optimize_circle(): #if something needs to be fixed
            self.optimize_radius()
        self.running_time = time.time() - starttime
        print("Time needed for optimization: ", self.running_time)
        print("Plotted Points:",self.number_of_points_to_create,"| Radius:",self.radius,"| Vector of center:",self.center)


    def scale_input(self,value_to_scale, mini=25,
                    maxi=60):  # make sure the number is between two values (25 and 60 for array size of the input)
        if value_to_scale <= mini:
            return mini  # crop any number to a definite min or max
        elif value_to_scale >= maxi:
            return maxi
        else:
            return value_to_scale

    def generate_random_array(self,size_of_final_array=24,
                              range_of_values=15):  # fill a list with random lists of values and return the list
        array_to_return = []
        for points in range(self.scale_input(size_of_final_array)):
            random_x = random.randint(-range_of_values, range_of_values)
            random_y = random.randint(-range_of_values, range_of_values)
            array_to_return.append((random_x, random_y))
        return array_to_return  # return the filled list

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

    def edgefinder(self, point):
        """This function will get all the points that border the cluster. We start at the point with the highest y-value. From that point we will
        measure to the left and probe all direction vektors of all points against a vektor that is determined by the quadrant out point is in. The point with the
        smallest angle has to be our next border point to the left. This will be done until we find our first point in our array of border points. This method can be improved by only testing aginst points in
        the own quadrant"""

        quadrant_this_point_is_in = self.get_quadrant(point)
        vector_to_test_against = []

        if quadrant_this_point_is_in is 1: #get the vector to test against
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
                #TODO: function could be improved by testing points in own quadrant first
                vector_between_the_two_points = np.array([point[0] - val[0], point[1] - val[1]])
                angle = self.get_angle_between_vectors(vector_to_test_against, vector_between_the_two_points)
                if angle < smallest_angle: # we get the smallest angle and then test with our new point
                    neighbour_point = val
                    smallest_angle = angle
        return neighbour_point

    def recursive_point_finding(self): #this function will call the edgefinder to fill up the arrays
        point_to_test = self.starting_point

        while point_to_test not in self.list_of_outer_points:
            self.list_of_outer_points.append(point_to_test)
            point_to_test = self.edgefinder(point_to_test)

        for x in self.list_of_outer_points:
            self.list_of_outer_x.append(x[0])
            self.list_of_outer_y.append(x[1])

    def set_first_radius_and_center(self): #find the two points that are furthest away and find the center between them
        for points in self.list_of_outer_points:
            for points_2 in self.list_of_outer_points:
                self.vector = np.array([(points_2[0] - points[0]), (points_2[1] - points[1])])
                rad = math.hypot(self.vector[0]/2,self.vector[1]/2)
                if rad > self.radius:
                    self.center = np.array(points + 0.5 * self.vector) #set center between furthest points as our first center
                    self.radius = rad
        self.origin_center = self.center
        self.origin_radius = self.radius

    def find_worst_error(self): #returns the point that is furthest of the radius
        worst_error = self.radius
        worst_point = []
        for point in self.list_of_outer_points:
            distance_to_center = self.get_length_of_vector(self.get_original_vector(point))
            if distance_to_center > self.radius and distance_to_center > worst_error:
                worst_error = distance_to_center
                worst_point = point
        return np.array(worst_point),worst_error

    def optimize_circle(self):
        #after we set our first center we find the points outside (if there are any) and take the worst
        #with the worst point we will calculate our new center
        worst_point,worst_point_dist = self.find_worst_error()
        if worst_point_dist == self.radius:
            self.was_already_perfect = 1
            return False
        unit_vec_of_worst_point = self.get_unit_vector(worst_point)
        margin_of_error = worst_point_dist - self.radius
        self.correction_vector = unit_vec_of_worst_point*margin_of_error
        self.origin_center = self.center
        self.center = self.center + self.correction_vector
        return True

    def optimize_radius(self):
        #when we switched our center we try to get the smallest radius possible
        worst_point, worst_point_dist = self.find_worst_error()
        self.origin_radius = self.radius
        self.radius = worst_point_dist

class plot_circle:
    #when we are done we throw all of our data against a simple plot
    #we plot our final circle, our first guess, our fist center, the new center and all the points
    def __init__(self,points_to_plot = 0):
        if points_to_plot is 0:
            self.points_to_plot = random.randint(25,60)
        else:
            self.points_to_plot =points_to_plot

        self.pointfinder = point_finder(self.points_to_plot)
        self.subplt = plt.subplot()

    def do_new_set(self):
        self.pointfinder = point_finder(self.points_to_plot)
        self.plot_results()

    def plot_results(self):
        self.subplt.scatter(self.pointfinder.list_of_x_vals, self.pointfinder.list_of_y_vals, s=10, facecolors='none', edgecolors='grey')
        self.subplt.scatter(self.pointfinder.list_of_outer_x, self.pointfinder.list_of_outer_y, s=10, facecolors='none', edgecolors='blue')
        self.subplt.scatter(self.pointfinder.center[0], self.pointfinder.center[1], s=20, facecolors='none', edgecolors='red')
        self.subplt.scatter(self.pointfinder.origin_center[0], self.pointfinder.origin_center[1], s=10, facecolors='none', edgecolors='black')
        self.subplt.add_patch(plt.Circle(self.pointfinder.center, self.pointfinder.radius, color='orange', alpha=0.4, fill=True))
        self.subplt.add_patch(plt.Circle(self.pointfinder.center, self.pointfinder.radius, color='red', alpha=1.0, fill=False))
        self.subplt.add_patch(plt.Circle(self.pointfinder.origin_center, self.pointfinder.origin_radius, color='blue', alpha=0.5, fill=False))
        self.subplt.set_aspect('equal', adjustable='datalim')
        self.subplt.plot()
        plt.show()




