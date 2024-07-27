#!/usr/bin/env python3
# coding: utf-8

'''
WebCamRecorder

Dependencies:
- pyautogui

Authors:
- Kayhan Latifzadeh <kayhan DOT latifzade AT_SYMBOL uni DOT lu>
'''


# Load std libs.
import numpy as np
import cv2 as cv
import time
import argparse
import os


parser = argparse.ArgumentParser(description='Record video from webcam',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--webcam_number', default=0, type=int,
                    help='the number of webcam, if you have more than 1 webcam')
parser.add_argument('--dir', default="",
                    help='directory to save the files (video, and log) in it')
parser.add_argument('--fid', default=f"webcam_rec_{int(time.time() * 1000)}",
                    help='file name for the recorded video and log file')
parser.add_argument('--filename_prefix', default="",
                    help='prefix for the file names (video, and log files)')
parser.add_argument('--filename_postfix', default="REC",
                    help='postfix for the file names (video, and log files)')

args = parser.parse_args()


# Load 3rd party libs.


def record_video(filename, webcam_number):

    log_file_path = f"{filename}.log"
    video_file_path = f"{filename}.mp4"

    log_file = open(log_file_path, 'w')

    timestamp = int(time.time() * 1000)

    capture = cv.VideoCapture(webcam_number)

    size = (int(capture.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv.CAP_PROP_FRAME_HEIGHT)))

    is_first_frame = True

    fourcc = cv.VideoWriter_fourcc(*'H264')
    out = cv.VideoWriter(video_file_path, fourcc, 30, size)
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            print("Stream is not available!")
            break
        # write the flipped frame
        out.write(frame)

        if is_first_frame:
            log_file.write(f'REC_STARTED {int(time.time() * 1000)}\n')
            is_first_frame = False

        cv.imshow('frame', cv.resize(frame, (320, 240)))
        if cv.waitKey(1) == ord('s'):
            log_file.write(f'REC_ENDED {int(time.time() * 1000)}\n')
            is_first_frame = False
            break

    capture.release()
    out.release()
    cv.destroyAllWindows()
    log_file.close()


if __name__ == "__main__":
    filename = args.fid
    if args.filename_prefix != "":
        filename = f"{args.filename_prefix}_{filename}"
    if args.filename_postfix != "":
        filename = f"{filename}_{args.filename_postfix}"
    record_video(filename=filename, webcam_number=args.webcam_number)
