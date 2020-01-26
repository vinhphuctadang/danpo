# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
OPENPOSE_INSTANCE = None

def init (params={}): # Should pass **kwarg, hah hah

	global OPENPOSE_INSTANCE

	if not OPENPOSE_INSTANCE:
		params["model_folder"] = "E:\\Python\\mypose\\examples\\tutorial_api_python\\lib\\models"
		# try:
		# Import Openpose (Windows/Ubuntu/OSX)
		dir_path = os.path.dirname(os.path.realpath(__file__))

		'''
			START SCOPE
			The following lines of code are adapted from openpose python example
			See project's details at: https://github.com/CMU-Perceptual-Computing-Lab/openpose/
		'''
		# Windows Import
		if platform == "win32":
			# Change these variables to point to the correct folder (Release/x64 etc.)
			# sys.path.append(dir_path + '/../../python/openpose/Release');
			print (dir_path)
			sys.path.append(dir_path + '/openpose/Release');
			os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/x64;' +  dir_path + '/bin;'
			import pyopenpose as OPENPOSE_INSTANCE
		else:
			# Change these variables to point to the correct folder (Release/x64 etc.)
			sys.path.append('/openpose/Release');
			# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
			# sys.path.append('/usr/local/python')
			import pyopenpose as OPENPOSE_INSTANCE
	'''
		END SCOPE
	'''
	# initialization for all utilities
	opWrapper = OPENPOSE_INSTANCE.WrapperPython()
	opWrapper.configure(params)
	opWrapper.start()

	return opWrapper

# only call to this function after init () had been called
def getBodySkeleton (opWrapper, imageToProcess): 
	datum = OPENPOSE_INSTANCE.Datum()
	datum.cvInputData = imageToProcess
	opWrapper.emplaceAndPop([datum])
	return datum

'''
	main () is just a test function 
'''
def main ():

	wrapper = init ()
	datum = getBodySkeleton (wrapper, cv2.imread ('samples/sample.jpg')) 
	print("Body keypoints: \n" + str(datum.poseKeypoints))
	cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
	cv2.waitKey(0)

if __name__=='__main__':
	main ()
# except Exception as e:
# 	print(e)
# 	sys.exit(-1)
