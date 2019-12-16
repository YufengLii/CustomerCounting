import sys
import os
import time
import numpy as np
import cv2
from shapely.geometry import Point
from tracker import Tracker
from my_utils import geometry, cvdraw
from modules.dbutil import MySQLPlugin


dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append('/home/feng/Documents/openpose/build/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?'
    )
    raise e

# frame_url = 'rtsp://admin:helab401@192.168.31.124/Streaming/Channels/101'
frame_url = '/home/feng/Videos/124_3.mp4'

canteen_human_num = 4

area_id = 0
db = MySQLPlugin()

db.update_headcount(area_id, canteen_human_num, int(time.time()*1000))

def tracking_human(tracked_positions, frame, canteen_human_num):
    tracker = Tracker(100, 50, 5)
    track_colors = [(0, 0, 255), (0, 255, 0), (255, 127, 255),  (255, 0, 0),
                    (255, 255, 0), (127, 127, 255), (255, 0, 255),
                    (127, 0, 255), (127, 0, 127), (127, 10, 255),
                    (0, 255, 127)]

    for i in range(len(tracked_positions)):
        centers = np.array(tracked_positions[i])
        if (len(centers) > 0):
            tracker.update(centers)
            for j in range(len(tracker.tracks)):
                if (len(tracker.tracks[j].trace) > 1):
                    x = int(tracker.tracks[j].trace[-1][0, 0])
                    y = int(tracker.tracks[j].trace[-1][0, 1])
                    tl = (x - 10, y - 10)
                    br = (x + 10, y + 10)
                    cv2.rectangle(frame, tl, br, track_colors[j], 1)
                    cv2.putText(frame, str(tracker.tracks[j].trackId),
                                (x - 10, y - 20), 0, 0.5, track_colors[j], 2)
                    for k in range(len(tracker.tracks[j].trace)):
                        x = int(tracker.tracks[j].trace[k][0, 0])
                        y = int(tracker.tracks[j].trace[k][0, 1])
                        cv2.circle(frame, (x, y), 3, track_colors[j], -1)
                    cv2.circle(frame, (x, y), 6, track_colors[j], -1)
    for tacker_i in tracker.tracks:
        distance = tacker_i.trace[-1][0, 0] - tacker_i.trace[0][0, 0]
        if distance > 100:
            db.update_headcount(area_id, canteen_human_num, int(time.time()*1000))
            canteen_human_num -= 1
            print("human out, total number is: " + str(canteen_human_num))
        elif distance < -100:
            db.update_headcount(area_id, canteen_human_num, int(time.time()*1000))
            canteen_human_num += 1
            print("human in, total number is: " + str(canteen_human_num))

            # print(tracker.tracks[j].trace[-1][0,0])
            # print(tracker.tracks[j].trace[-1][0,1])
            # cv2.circle(frame,(int(tracked_positions[i][j][0]),int(tracked_positions[i][j][1])), 6, (0,0,0),-1)
            # cv2.imshow('image',frame)
            # cv2.imwrite("image"+str(i)+".jpg", frame)
            # images.append(imageio.imread("image"+str(i)+".jpg"))
            # time.sleep(0.1)
            # cv2.waitKey(1)
    # imageio.mimsave('Multi-Object-Tracking.gif', images, duration=0.08)


def canteen_human_count():

    params = dict()
    params["model_folder"] = "/home/feng/Documents/openpose/models/"
    params["model_pose"] = "BODY_25"
    params["net_resolution"] = "656x368"
    # params["tracking"] = 0
    # params["number_people_max"] = 1

    try:
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()
    except Exception as e:
        print("opWrapper init error!!!")
        print(e)
        sys.exit(-1)

    vidcap = cv2.VideoCapture(frame_url)
    datum = op.Datum()

    t0 = time.time()
    run_num = 1

    tracked_positions = []
    tracking_state = False
    while True:
        run_num += 1
        if run_num == 100:
            print('run fps: ' + str(1 / ((time.time() - t0) / 100)))
            t0 = time.time()
            run_num = 1
        success, image = vidcap.read()
        if success:
            img_test2 = cv2.resize(image, (0, 0),
                                   fx=0.5,
                                   fy=0.5,
                                   interpolation=cv2.INTER_NEAREST)
            datum.cvInputData = img_test2
            opWrapper.emplaceAndPop([datum])
            frame_keypoints = datum.poseKeypoints
            # image_out = datum.cvOutputData
            cvdraw.draw_rect(img_test2, (241, 1), (437, 1), (236, 600),
                             (40, 600))
            curr_frame_tracking = []

            if len(frame_keypoints.shape) == 0:
                curr_frame_tracking.append(-1)
                #Sprint(curr_frame_tracking)
                continue

            for human_keypoints in frame_keypoints:
                RShoulder = human_keypoints[2]
                LShoulder = human_keypoints[5]
                if RShoulder[2] > 0.3 or LShoulder[2] > 0.3:

                    area = [(241, 1), (437, 1), (236, 600), (40, 600)]

                    if RShoulder[1] > LShoulder[1]:
                        position_x = RShoulder[0]
                        position_y = RShoulder[1]
                    else:
                        position_x = LShoulder[0]
                        position_y = LShoulder[1]

                    if geometry.is_in_square_table(
                            area, Point(position_x, position_y)) is True:
                        cv2.circle(img_test2, (position_x, position_y), 10,
                                   (0, 0, 255), -1)
                        curr_frame_tracking.append([position_x, position_y])

            if curr_frame_tracking == []:
                curr_frame_tracking.append(-1)
        else:
            print('read fail')
        #print(curr_frame_tracking)

        if curr_frame_tracking != [-1]:
            if tracked_positions == []:
                print('tracking started')
            tracking_state = True
            tracked_positions.append(curr_frame_tracking)
        else:

            if tracking_state is True:
                print('tracking stoped')
                #print('cal in out ----------------------')
                #print(tracked_positions)
                #inout_judge(tracked_positions,canteen_human_num)
                tracking_human(tracked_positions, img_test2, canteen_human_num)
                tracked_positions = []
                tracking_state = False
            else:
                tracked_positions = []
                tracking_state = False

        cv2.imshow("image", img_test2)
        cv2.waitKey(1)


canteen_human_count()
