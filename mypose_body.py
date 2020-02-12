# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import json
# from json import encoder
# encoder.FLOAT_REPR = lambda o: format(o, '.2f')
dir_path = os.path.dirname(os.path.realpath(__file__))
# Giả sử %OPENPOSE% là đường dẫn, dẫn đến thư mục OPENPOSE đã được dựng. VD: D:\build\OPENPOSE\
OPENPOSE_INSTANCE   = None
OPENPOSE_MODELS 	= dir_path + "/models/" #Đổi thành đường dẫn đến các models của OPENPOSE
OPENPOSE_RELEASE_PY = dir_path + '/openpose/Release' # Đổi thành đường dẫn, đẫn đến %OPENPOSE%/Release
OPENPOSE_x64 	    = dir_path + '/x64';
OPENPOSE_BIN		= dir_path + '/bin';

# init () là code của openpose_python_api_example, mình dựa vào để phát triển
def init (params={}): # Should pass **kwarg, hah hah
	global OPENPOSE_INSTANCE

	if not OPENPOSE_INSTANCE:
		
		# try:
		# Import Openpose (Windows/Ubuntu/OSX)
		if not "model_folder" in params:
			
			params["model_folder"] = OPENPOSE_MODELS
		'''
			Mấy dòng này của mình, chém gió tiếng anh vậy thôi, m.n. thông cảm
			START SCOPE
			The following lines of code are adapted from openpose python api example
			See details of the project at: https://github.com/CMU-Perceptual-Computing-Lab/openpose/
		'''
		# Windows Import
		if platform == "win32":
			# Change these variables to point to the correct folder (Release/x64 etc.)
			# sys.path.append(dir_path + '/../../python/openpose/Release');
			# print (dir_path)
			sys.path.append(OPENPOSE_RELEASE_PY);
			os.environ['PATH'] = os.environ['PATH'] + ';' + OPENPOSE_x64 +  ';' + OPENPOSE_BIN + ';'
			import pyopenpose as OPENPOSE_INSTANCE
			# print (OPENPOSE_INSTANCE.__file__)
		else:
			# Change these variables to point to the correct folder (Release/x64 etc.)
			sys.path.append(OPENPOSE_RELEASE_PY);
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

# def savePose (pose, file_name='output.csv'):
# 	f = open (file_name, 'w');
# 	for pnt in pose:
# 		_l_ = len (pnt)
# 		for v in range (_l_):
# 			f.write (str (pnt[v]))
# 			if (v < _l_ - 1):
# 				f.write (',')
# 		f.write ('\n')
# 	f.close ()

'''
	pose extract steps:
	
	1. Read image
	2. Extract pose
	3. Find desired file to store poses
		the poses will be stored as json into the file named <file_original_name>.json
'''

def toList (poses):
	result = []
	for eachPose in poses:
		pose = []
		for eachPoint in eachPose:
			# print (list (eachPoint))
			dim = [round (float (x), 3) for x in eachPoint]
			pose.append (dim)

		result.append (pose)
	return result

def poseExtract (wrapper, path): 
	
	img = cv2.imread (path)
	datum = getBodySkeleton (wrapper, img)

	dirname = os.path.dirname (path)
	filename = os.path.basename (path)
	parts = os.path.splitext(filename)
	name_only = parts[0]
	
	POSE_FOLDER = dirname + '/pose'
	if not os.path.isdir (POSE_FOLDER):
		os.mkdir (POSE_FOLDER)
		
	# count = 0
	if datum.poseKeypoints.shape == ():
		return datum
		
	dest_file = '%s/%s.json' % (POSE_FOLDER, name_only)

	_ = {
		'size' : tuple(img.shape[1::-1]),
		'pose' : toList (datum.poseKeypoints) 
	}
	with open (dest_file, 'w') as f:
		jstr = json.dumps (_, indent=' ')
		f.write (jstr)
	
	return datum

def main ():


	wrapper = init ({
		# 'hand': True,
		# 'pose': False,
		'render_pose' : 0
		})

	'''
		'path' là đường dẫn trỏ đến thư mục chứa các khung hình của video (các khung hình được tách ra được nhờ frame_extractor.py trong ~/danca/tools/)
		mình nên để đường dẫn tuyệt đối cho đỡ nhầm, mặc dù cũng không tốt lắm		
	'''
	path = './samples/'; # Sửa chỗ này để dẫn đến các khung hình (frame)
	root, dirs, files = next (os.walk (path))
	from time import time
	print ('Start pose detecting in frames ...')
	for file in files:
		if file.find ('.csv')>-1:
			continue
		print ('Pose extraction of', file, end='... ')
		marked = time ()
		datum = poseExtract (wrapper, path+'/'+file)
		# cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
		# cv2.waitKey(0)
		print ('done, after', time () - marked)
		# break

if __name__=='__main__':
	main ()
