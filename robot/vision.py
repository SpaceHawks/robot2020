#vision.py
from hokuyolx import HokuyoLX
import numpy as np
import math

#superclass for Locater and Detector
class SpacehawksHokuyoLXWrapper:

	def __init__(self):
		self.lidar = HokuyoLX()

	def get_dists(self):
		return self.lidar.get_filtered_dist()[1].tolist()

	def get_intens(self):
		return self.lidar.get_filtered_intens()[1].tolist()

#for an object that represents a lidar used for location tracking
class SpacehawksHokuyoLXLocater(SpacehawksHokuyoLXWrapper):

	REFLECTIVITY_THRESHOLD = 3000
	
	def __init__(self):
		# default constructor for locater object
		super().__init__()
		self.x_coordinate = 0.0
		self.y_coordinate = 0.0
		self.orientation = 0.0

	def update(self):
		REFLECTIVITY_THRESHOLD = SpacehawksHokuyoLXLocater.REFLECTIVITY_THRESHOLD
		# get a python list of all data-points with angle, dist,
		#	and reflective intensity
		data_points = super().get_intens()
		
		# detect using an FSM to find the changing points on target
		list_of_target_points = []
		# True -  Target is |Bright|Black|Bright|Black|
		# False - Target is |Black|Bright|Black|Bright|
		looking_for_brighter = True
		points_left = 3 	# we only want 3 points
		for data_point in data_points:
			if looking_for_brighter and points_left > 0:
				if data_point[2] > REFLECTIVITY_THRESHOLD:
					list_of_target_points.append(data_point)
					looking_for_brighter = False
					points_left -= 1
			elif points_left > 0:
				if data_point[2] < REFLECTIVITY_THRESHOLD:
					list_of_target_points.append(data_point)
					looking_for_brighter = True
					points_left -= 1
					
		#FIXME debugging print statement
		# print("list of target points")
		# print(list_of_target_points)
		# print("___________________________________________")
		
		
		distance_to_origin = list_of_target_points[1][1]
		origin_point_angle = list_of_target_points[1][0]
		distance_to_helper = list_of_target_points[0][1]
		angle_difference = abs(list_of_target_points[1][0] - list_of_target_points[0][0])
		
		# we have to calculate stripe width because the readings
		#	aren't 100% accurate
		stripe_width = math.sqrt((distance_to_origin**2)+(distance_to_helper**2)-(2*distance_to_helper*distance_to_origin*math.cos(angle_difference)))
		
		#FIXME debugging print statement
		# print("stripe width:\t\t" + str(stripe_width))
		
		origin_angle = abs(math.asin((distance_to_helper*math.sin(angle_difference))/stripe_width))
		x_factor = -1 
		
		#FIXME debugging print statement
		# print("origin angle:\t\t" + str(origin_angle * (180/math.pi)))
		# print("origin point angle:\t" + str(origin_point_angle * (180/math.pi)))
		# print("___________________________________________")
		
		# x_factor will modify the calculated x-coord depending on angle of
		# 	origin data point
		if origin_point_angle < 0:
			x_factor = 1
		x_coordinate = distance_to_origin*math.cos(origin_angle) * x_factor
		y_coordinate = distance_to_origin*math.sin(origin_angle)
		
		# calculate orientation
		orientation = (math.pi/2) - origin_angle - origin_point_angle
		
		# assign calculated values to the properties of the locater
		self.x_coordinate = x_coordinate
		self.y_coordinate = y_coordinate
		self.orientation = orientation

	def getX(self):
		return self.x_coordinate

	def getY(self):
		return self.y_coordinate

	def getOrientation(self):
		return self.orientation

# tests for SpacehawksHokuyoLXLocater class
def test_locater():
	locater= SpacehawksHokuyoLXLocater()
	locater.update()
	print("x-coord:\t\t" + str(locater.getX()))
	print("y-coord:\t\t" + str(locater.getY()))
	print("orientation:\t\t" + str(locater.getOrientation() * (180/math.pi)))
	return
		
#for a lidar used for obstacle detection
class SpacehawksHokuyoLXDetector(SpacehawksHokuyoLXWrapper):
	def __init__(self):
		super().__init__()
		self.danger_points = []
		
	def update(self):
		# get all points from the basic get_dist() function
		all_points = super().get_dist()
		
		# narrow them down with trig and filtering
		
		#for every point in all_points
		for data_point in all_points:
			# calculate what an acceptable height deviance is
			# calculate the height of this data point
			# compare: if greater than threshold,calculate the coord and add to prelim_danger_coords
			pass
		# give prelim_danger_coords to danger_coords
		
		return
		
	def get_danger_coords(self):
		#return python 2d list of danger coords
		pass

#test code	
print("")
print("___________________________________________")
print("___________________________________________")
	
test_locater()

print("___________________________________________")
print("___________________________________________")
print("")