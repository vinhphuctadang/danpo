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
		
		# try:
		# Import Openpose (Windows/Ubuntu/OSX)
		if not "model_folder" in params:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			params["model_folder"] = dir_path + "/models/"
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
			os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/x64;' +  dir_path + '/bin;'
			import pyopenpose as OPENPOSE_INSTANCE
			print (OPENPOSE_INSTANCE.__file__)
		else:
			# Change these variables to point to the correct folder (Release/x64 etc.)
			# sys.path.append('./openpose/Release');
			# print (sys.path)
			# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
			sys.path.append('/usr/local/python')
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

def savePose (pose, file_name='output.csv'):
	f = open (file_name, 'w');
	for pnt in pose:
		_l_ = len (pnt)
		for v in range (_l_):
			f.write (str (pnt[v]))
			if (v < _l_ - 1):
				f.write (',')
		f.write ('\n')
	f.close ()


'''
	pose extract steps:
	
	1. Read image
	2. Extract pose
	3. Find desired file to store poses
		the poses will be stored as csv into the file named <file_original_name>_pose<pose_number>.csv
'''
def poseExtract (wrapper, path): 
	
	img = cv2.imread (path);
	datum = getBodySkeleton (wrapper, img)

	dirname = os.path.dirname (path)
	filename = os.path.basename (path)
	parts = os.path.splitext(filename)
	name_only = parts[0]
	
	count = 0
	if datum.poseKeypoints.shape == ():
		return datum
		
	for pose in datum.poseKeypoints:
		dest_file = '%s/%s_pose%02d.csv' % (dirname, name_only, count);
		savePose (pose, dest_file);
		count += 1
	return datum
'''
	main () is just a test function 
'''
def main ():


	wrapper = init ({
		# 'hand': True,
		# 'pose': False,
		# 'render_pose' : 0
		})

	# print (str (OPENPOSE_INSTANCE.init_argv))
	# print (dir (OPENPOSE_INSTANCE))
	# print (dir (wrapper))
	
	# from time import time

	# marked = time ()

	# datum = poseExtract (wrapper, './samples/sample (4).jpg')
	# cv2.imshow ('Danpo', datum.cvOutputData)
	# cv2.waitKey (0)

	path = './samples/';
	root, dirs, files = next (os.walk (path))
	from time import time

	for file in files:
		if file.find ('.csv')>-1:
			continue
		print ('Pose extraction of', file, end='... ')
		marked = time ();
		datum = poseExtract (wrapper, path+'/'+file)
		cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
		cv2.waitKey(1)
		print ('done, after', time () - marked)
		# break

	#	print("Body keypoints: \n" + str(datum.poseKeypoints))
	# 	print("Hand keypoints: " + str (datum.handKeypoints))
	# 	cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
	# 	cv2.waitKey(0)
	# 	break

	# print ('total time consumed:', time () - marked)
	# print (dir (datum))
	# print (datum.faceRectangles)



if __name__=='__main__':
	main ()
# except Exception as e:
# 	print(e)
# 	sys.exit(-1)
