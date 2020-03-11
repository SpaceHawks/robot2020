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

lidar = Wrapper()

intens = lidar.get_intens()

angles = [round(intens[a][0] * 180 / math.pi, 2) for a in range(len(intens))]
print(angles)
