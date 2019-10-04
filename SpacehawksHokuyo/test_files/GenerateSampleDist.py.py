from hokuyolx import HokuyoLX
import numpy as np

def generateSampleDist():

	lidar = HokuyoLX()

	_, data = lidar.get_filtered_dist()

	data=data.tolist()

	fileName = input("Enter a file name: ")

	with open(str(fileName) + ".txt", 'w') as pw:
		for i in range(len(data)):
			pw.write(str(data[i][0]) + "," + str(data[i][1]))
			if i != len(data)-1:
				pw.write("\n")
			pw.close()
	lidar.close()

#Writes to the file line by line comma delimmited angles then distances
