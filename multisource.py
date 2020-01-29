#!/usr/bin/python3
#!--*-- coding:utf-8 --*--
#! Author: Tim Chan, motoleisure@gmail.com

import cv2
import time
import os.path
import sys
import argparse
import numpy as np
from openpose import pyopenpose as op

def readCap(args):
    outputFile = "openpose_out_py.mp4"

    if (args.image):
        # Open the image file
        if not os.path.isfile(args.image):
            print("Input image file ", args.image, " doesn't exist")
            sys.exit(1)
        cap = cv2.VideoCapture(args.image)
        outputFile = args.image[:-4]+'_openpose_out_py.jpg'
    elif (args.video):
        # Open the video file
        if not os.path.isfile(args.video):
            print("Input video file ", args.video, " doesn't exist")
            sys.exit(1)
        cap = cv2.VideoCapture(args.video)
        outputFile = args.video[:-4]+'_openpose_out_py.mp4'
    else:
        # Webcam input
        cap = cv2.VideoCapture(0)

        cap.set(3, 720)
        cap.set(4, 1280)

    return cap, outputFile

def processing_openpose(args):

    # Initialize the openpose parameters
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = {}
    params["model_folder"] = "/home/ares2/openpose/models"
    params["hand"] = True

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # cv2 display setups
    winName = 'Deep learning object detection in OpenCV'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)

    cap, outputFile = readCap(args)

    # Get the video writer initialized to save the output video
    if (not args.image):
        vid_writer = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                     30, (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                          round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while cv2.waitKey(1) < 0:
        start_time = time.time()
        # get frame from the video
        hasFrame, frame = cap.read()

        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            print("Output file is stored as ", outputFile)
            cv2.waitKey(3000)
            # Release device
            cap.release()
            break

        # openpose input
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop([datum])

        # openpose output
        frame = datum.cvOutputData
        end_time = time.time()
        t = end_time - start_time
        label = 'Inference time: %.2f ms' % ( 1.0 / t)
        cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        # Write the frame with the detection boxes
        if (args.image):
            cv2.imwrite(outputFile, frame.astype(np.uint8))
        else:
            vid_writer.write(frame.astype(np.uint8))

        cv2.imshow(winName, frame)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Openpose Python API usage example')
    parser.add_argument('--image', help='Path to image file.')
    parser.add_argument('--video', help='Path to video file.')
    args = parser.parse_args()

    processing_openpose(args)