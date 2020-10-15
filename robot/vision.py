#vision.py
from hokuyolx import HokuyoLX
import numpy as np
import math
import sys
from termcolor import colored, cprint


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
		self.outlierConstant = 1.5

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

		os = []
		ys = []
		for k in range(len(targets) - 1):
			t1 = targets[k]
			t2 = targets[k+1]
			(_o, _y) = self.target_xy(t1, t2)
			os.append(_o)
			ys.append(_y)

		return (os, ys)

	def removeOutliers(self, x):
		# Removes outliers before taking the average
		pos = 0
		a = np.array(x)
		upper_quartile = np.percentile(a, 75)
		lower_quartile = np.percentile(a, 25)
		IQR = (upper_quartile - lower_quartile) * self.outlierConstant
		quartileSet = (lower_quartile - IQR, upper_quartile + IQR)

		y_sum = 0
		count = 0
		for y in a:
			if y >= quartileSet[0] and y <= quartileSet[1]:
				y_sum += y
				count += 1

		return y_sum / count if count > 0 else 0

	def target_xy(self, t1, t2):
		[angle1, d1, _] = t1
		[angle2, d2, _] = t2

		theta = abs(angle1 - angle2)

		stripe_width = math.sqrt((d1**2)+(d2**2)-(2*d1*d2*math.cos(theta)))

		# alpha = math.asin(d1 * math.sin(theta) / stripe_width)

		y = d1 * d2 * math.sin(theta) / stripe_width

		side_of_target = 1 if d1 < d2 else -1 # 1 if right of target

		sign = 1 if angle1 >= 0 else -1 # 1 if robot pointing right, 0 if pointing left

		orientation = sign * abs(side_of_target * angle1 - math.acos(y/d1))

		def toDeg(x):
			return colored(str(round(x * 180 / math.pi, 2)) + ' deg', 'green')

		def toCM(x):
			return colored(str(round(x / 10, 2)) + ' cm', 'green')

		print(f"d1: {toCM(d1)}, a1: {toDeg(angle1)}")
		print(f"d2: {toCM(d2)}, a2: {toDeg(angle2)}")
		print(f"o1: {toDeg(orientation)}")
		print(f"y: {toCM(y)}\n")

		# print(f"orientation1: {orientation * 180 / math.pi}, orientation2: {orientation2 * 180 / math.pi}")
		# print(orientation * 180 / math.pi, "deg")``
		return (orientation, y)

	def update(self):
		ITERATIONS = 10

		os = []
		ys = []

		for i in range(ITERATIONS):
			(_os, _ys) = self.single_run();
			os += _os
			ys += _ys

		y_avg = self.removeOutliers(ys)
		o_avg = self.removeOutliers(os)

		print(f"o: {round(o_avg * 180 / math.pi, 2)} degrees")
		print(f"y: {round(0.1 * y_avg, 2)} cm")


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
