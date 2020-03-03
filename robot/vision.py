#vision.py
from hokuyolx import HokuyoLX
import numpy as np
import math

#superclass for Locater and Detector
class Wrapper:

	def __init__(self):
		self.lidar = HokuyoLX()

	def get_dists(self):
		return self.lidar.get_filtered_dist()[1].tolist()

	def get_intens(self):
		return self.lidar.get_filtered_intens()[1].tolist()

#for an object that represents a lidar used for location tracking
class Locater(Wrapper):
	def __init__(self):
		super().__init__()
		self.x_coordinate = 0.0
		self.y_coordinate = 0.0
		self.orientation = 0.0

	def update(self):
		# How reflective is the light part of the target?
		REFLECTIVITY_THRESHOLD = 3000

		# Returns [(angle, distance, intensity), ...]
		data_points = super().get_intens()
		looking_for_brighter = True
		targets = []
		points_left = 3

		"""
		Store into targets:
		1. Find first bright point [0]
		2. Find next dark point [1]
		3. Find next bright point [2]
		"""
		for point in data_points:
			if points_left <= 0:
				break
			if looking_for_brighter:
				if point[2] > REFLECTIVITY_THRESHOLD:
					targets.append(point)
					looking_for_brighter = False
					points_left -= 1
			else:
				if point[2] < REFLECTIVITY_THRESHOLD:
					targets.append(point)
					looking_for_brighter = True
					points_left -= 1
		else:
			# else: on for-loop = "if break not called in for loop:"
			# Target not found, should probably raise an exception or sumn
			print("Target not found")
			return

		distance_to_origin = targets[1][1] # Dark point distance
		distance_to_helper = targets[0][1] # First light point distance

		angle1 = targets[1][0] # Dark point angle
		angle2 = targets[0][0] # Light point angle

		angle_difference = abs(angle1 - angle2)

		# TODO: This should be used to verify that we are looking at the correct area
		#		it should be really close to the actual stripe width

		# Calculate via Law of Cosines
		stripe_width = math.sqrt((distance_to_origin**2)+(distance_to_helper**2)-(2*distance_to_helper*distance_to_origin*math.cos(angle_difference)))

		# Math proof here https://drive.google.com/file/d/1Imi_5TYSH6YQEKciQ27xJUhhHKdNim4q/view
		origin_angle = abs(math.asin((distance_to_helper*math.sin(angle_difference))/stripe_width))

		# Correct for sign
		x_factor = -1
		if origin_angle > math.pi / 2:
			x_factor = 1
			origin_angle = math.pi - origin_angle
		x_coordinate = distance_to_origin*math.cos(origin_angle) * x_factor
		y_coordinate = distance_to_origin*math.sin(origin_angle)

		print(f"x:{x_coordinate} mm, y:{y_coordinate} mm, a: {origin_angle}")
		print(f"a1:{angle1 * 180 / math.pi}, a2: {angle2 * 180 / math.pi}")

		# TODO: Finish adding orientation
		#orientation = math.pi / 2 - angle1 - origin_angle

		self.x_coordinate, self.y_coordinate, self.orientation = x_coordinate, y_coordinate, orientation

	def getX(self):
		return self.x_coordinate

	def getY(self):
		return self.y_coordinate

	def getOrientation(self):
		return self.orientation

#for a lidar used for obstacle detection
class Detector(Wrapper):
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
variable = Locater()
variable.update()
