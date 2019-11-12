#vision.py
from hokuyolx import HokuyoLX
import numpy as np

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

	def __init__(self):
		super().__init__()
		self.x_coordinate = 0.0
		self.y_coordinate = 0.0
		self.orientation = 0.0

	def update(self):
		REFLECTIVITY_THRESHOLD = 3000
		data_points = super().get_intens()
		looking_for_brighter = True
		list_of_target_points = []
		points_left = 3
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
		print(list_of_target_points)


	def getX(self):
		return self.x_coordinate

	def getY(self):
		return self.y_coordinate

	def getOrientation(self):
		return self.orientation

#for a lidar used for obstacle detection
class SpacehawksHokuyoLXDetector(SpacehawksHokuyoLXWrapper):
	pass

#test code
# variable = SpacehawksHokuyoLXLocater()
# variable.update()