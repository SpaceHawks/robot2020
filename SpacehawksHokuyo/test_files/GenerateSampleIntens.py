from hokuyolx import HokuyoLX
import numpy as np

def generateSampleDist():

	lidar = HokuyoLX()

	_, data = lidar.get_filtered_intens()

	data=data.tolist()

	fileName = input("Enter a file name: ")

	with open(str(fileName) + ".txt", 'w') as pw:
		for i in range(len(data)):
			pw.write(str(data[i][0]) + "," + str(data[i][1]) + "," + str(data[i][2]))
			if i != len(data)-1:
				pw.write("\n")
		
	lidar.close()

#Writes to the file line by line comma delimmited angles then distances then intensities

generateSampleDist()