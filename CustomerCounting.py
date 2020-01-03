# -*- coding: utf-8 -*-
import sys
import time
import cv2
from multiprocessing import Process, Queue
from my_utils import algorithm, config
from shapely.geometry import Point

try:
    sys.path.append('/home/feng/Documents/openpose/build/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found.')
    raise e


def canteen_human_count():
    canteen_human_num = config.canteen_human_num_init
    enter_num = config.enter_num_init
    depart_num = config.depart_num_init
    params = config.op_params
    frame_url = config.frame_url
    line_x_min = config.line_x_min
    line_x_max = config.line_x_max
    line_y_max = config.line_y_max
    line_y_min = config.line_y_min
    area_id = config.area_id

    try:
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()
    except Exception as e:
        print("opWrapper init error!!!")
        print(e)
        sys.exit(-1)

    datum = op.Datum()
    t0 = time.time()
    run_num = 1
    tracked_positions = []
    tracking_state = False
    fps = 0

    vidcap = cv2.VideoCapture(frame_url)

    while True:
        run_num += 1
        if run_num == 200:
            fps = 1 / ((time.time() - t0) / 100)
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

            cv2.line(img_test2, (line_x_min, line_y_min),
                     (line_x_min, line_y_max), (250, 0, 1), 2)
            cv2.line(img_test2, (line_x_max, line_y_min),
                     (line_x_max, line_y_max), (0, 0, 255), 2)

            curr_frame_tracking = []

            if len(frame_keypoints.shape) == 0:
                curr_frame_tracking.append(-1)
                cv2.putText(
                    img_test2,
                    "Canteen human number:  " + (str)(canteen_human_num),
                    (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img_test2, "fps:  " + (str)(
                    (int)(fps)), (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                cv2.putText(img_test2, "Enter number:  " + (str)(enter_num),
                            (800, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                cv2.putText(img_test2, "Depart number:  " + (str)(depart_num),
                            (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                cv2.imshow("image", img_test2)
                cv2.waitKey(1)
                continue

            for human_keypoints in frame_keypoints:
                RShoulder = human_keypoints[2]
                LShoulder = human_keypoints[5]
                # Neck = human_keypoints[1]

                area = [(line_x_min, line_y_min), (line_x_max, line_y_min),
                        (line_x_max, line_y_max), (line_x_min, line_y_max)]

                # if Neck[2] > 0.3:
                #     position_x = Neck[0]
                #     position_y = Neck[1]

                if RShoulder[2] > 0.1 or LShoulder[2] > 0.1:

                    area = [(line_x_min, line_y_min), (line_x_max, line_y_min),
                            (line_x_max, line_y_max), (line_x_min, line_y_max)]

                    if RShoulder[1] > LShoulder[1]:
                        position_x = RShoulder[0]
                        position_y = RShoulder[1]
                    else:
                        position_x = LShoulder[0]
                        position_y = LShoulder[1]

                    if algorithm.is_in_square_table(
                            area, Point(position_x, position_y)) is True:
                        # cv2.circle(img_test2, (position_x, position_y), 10,
                        #            (0, 0, 255), -1)
                        curr_frame_tracking.append([position_x, position_y])

            if curr_frame_tracking == []:
                curr_frame_tracking.append(-1)

            if curr_frame_tracking != [-1]:
                if tracked_positions == []:
                    print('tracking started')
                tracking_state = True
                tracked_positions.append(curr_frame_tracking)
            else:
                if tracking_state is True:
                    print('tracking stoped')
                    num_changed, enter_num_, depart_num_, img_test2 = algorithm.tracking_human(
                        tracked_positions, img_test2)
                    cv2.imshow("image", img_test2)
                    cv2.waitKey(1000)
                    canteen_human_num = canteen_human_num + num_changed
                    if canteen_human_num < 0:
                        canteen_human_num = 0
                    if num_changed > 0:
                        enter_num = enter_num + enter_num_
                        msg_str = {
                            'areaID': area_id,
                            'enter': enter_num,
                            'depart': 0,
                            'timestamp': int(time.time() * 1000),
                            'num': canteen_human_num,
                        }
                        print(msg_str)

                    elif num_changed < 0:
                        depart_num = depart_num_ + depart_num
                        msg_str = {
                            'areaID': area_id,
                            'enter': 0,
                            'depart': depart_num,
                            'timestamp': int(time.time() * 1000),
                            'num': canteen_human_num,
                        }
                        print(msg_str)

                    print("human number is: " + str(canteen_human_num))
                    tracked_positions = []
                    tracking_state = False
                else:
                    tracked_positions = []
                    tracking_state = False
            cv2.putText(img_test2, "fps:  " + (str)((int)(fps)), (800, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_test2,
                        "Canteen human number:  " + (str)(canteen_human_num),
                        (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_test2, "Enter number:  " + (str)(enter_num),
                        (800, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)
            cv2.putText(img_test2, "Depart number:  " + (str)(depart_num),
                        (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)
        else:
            print('read frame fail')
            vidcap.release()
            time.sleep(5)
            vidcap = cv2.VideoCapture(frame_url)
        cv2.imshow("image", img_test2)
        cv2.waitKey(1)


canteen_human_count()
