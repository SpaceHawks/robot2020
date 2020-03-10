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

	def single_run(self):
		# How reflective is the light part of the target?
		REFLECTIVITY_THRESHOLD = 3000

		# get_intens() returns [(angle, distance, intensity), ...]
		data_points = super().get_intens()
		looking_for_brighter = True
		targets = []
		points_left = 6

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
			exit()
			return

		# Use all possible triangles to triangulate position
		y_avg = 0
		x_sum = 0
		count = 0
		for k in range(len(targets) - 1):
			t1 = targets[k]
			t2 = targets[k+1]
			(_x, _y) = self.target_xy(t1, t2)
			if y_avg != 0 and abs(_y - y_avg) > 0.25 * y_avg:
				pass
			else:
				y_avg = (y_avg * count + _y) / (count + 1)
				x_sum += _x
				count += 1

		x = x_sum / count

		return (x, y_avg)


	def target_xy(self, t1, t2):
		[angle1, d1, _] = t1
		[angle2, d2, _] = t2

		theta = abs(angle1 - angle2)

		stripe_width = math.sqrt((d1**2)+(d2**2)-(2*d1*d2*math.cos(theta)))

		# alpha = math.asin(d1 * math.sin(theta) / stripe_width)

		y = d1 * d2 * math.sin(theta) / stripe_width

		return (0, y)

	def update(self):
		ITERATIONS = 10

		sum_x = 0
		sum_y = 0

		for i in range(ITERATIONS):
			(_x, _y) = self.single_run();
			sum_x += _x
			sum_y += _y


		print(f"y: {round(0.1 * sum_y / ITERATIONS, 2)} cm")


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
