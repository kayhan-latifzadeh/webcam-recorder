import numpy as np
import cv2 as cv
import time
import sys

def record_video(filename):


    log_file_path = filename + '_REC.log'
    video_file_path = filename + 'REC.mp4'

    log_file = open(log_file_path, 'w')

    timestamp = int(time.time() * 1000)


    capture = cv.VideoCapture(0)

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
    if len(sys.argv) > 1 and sys.argv[1] == "-fid":
        if len(sys.argv) > 2:
            filename = sys.argv[2]
            record_video(filename)
        else:
            print("Please provide a filename after -fid.")
    else:
        print("Please use -fid followed by a filename to specify the output file.")
