# -*- coding: utf-8 -*-

from shapely.geometry.polygon import Polygon
import numpy as np
import cv2
from scipy.optimize import linear_sum_assignment
from collections import deque




# 判断点是否在四边形内

def is_in_square_table(table_coor, point):

    # table_coor,      按照顺时针方向的桌子顶点
    # point,           待计算点坐标 例，Point(Neck[0], Neck[1])
    # 调用实例
    # table_back = [(ellipse_cali_info['back_top_left'][0], ellipse_cali_info['back_top_left'][1]), (ellipse_cali_info['back_top_right'][0], ellipse_cali_info['back_top_right'][1]),
    # check_1 = is_in_square_table(table_back, Point(Neck[0], Neck[1]))

    polygon = Polygon(table_coor)
    inout = polygon.contains(point)
    if inout:
        return True
    else:
        return False




def tracking_human(tracked_positions, frame):
    num_change = 0
    enter_num_ = 0
    depart_num_ = 0

    tracker = Tracker(100, 10, 20)
    track_colors = [(0, 0, 255), (0, 255, 0), (255, 127, 255), (255, 0, 0),
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
        if len(tacker_i.trace) < 5:
            continue
        distance = tacker_i.trace[-1][0, 0] - tacker_i.trace[0][0, 0]
        # print(tacker_i.trace[-1][0, 0])
        # print(tacker_i.trace[0][0, 0])
        # print(distance)
        if distance > 50 and tacker_i.trace[-1][0, 0] > 200:
            num_change -= 1
            depart_num_ = depart_num_ + 1
            print("human out")
        elif distance < -50 and tacker_i.trace[-1][0, 0] < 200:
            enter_num_ = enter_num_ + 1
            num_change += 1
            print("human in")
    return num_change, enter_num_, depart_num_, frame



class KalmanFilter(object):
	"""docstring for KalmanFilter"""

	def __init__(self, dt=1,stateVariance=1,measurementVariance=1, 
														method="Velocity" ):
		super(KalmanFilter, self).__init__()
		self.method = method
		self.stateVariance = stateVariance
		self.measurementVariance = measurementVariance
		self.dt = dt
		self.initModel()
	
	"""init function to initialise the model"""
	def initModel(self): 
		if self.method == "Accerelation":
			self.U = 1
		else: 
			self.U = 0
		self.A = np.matrix( [[1 ,self.dt, 0, 0], [0, 1, 0, 0], 
										[0, 0, 1, self.dt],  [0, 0, 0, 1]] )

		self.B = np.matrix( [[self.dt**2/2], [self.dt], [self.dt**2/2], 
																[self.dt]] )
		
		self.H = np.matrix( [[1,0,0,0], [0,0,1,0]] ) 
		self.P = np.matrix(self.stateVariance*np.identity(self.A.shape[0]))
		self.R = np.matrix(self.measurementVariance*np.identity(
															self.H.shape[0]))
		
		self.Q = np.matrix( [[self.dt**4/4 ,self.dt**3/2, 0, 0], 
							[self.dt**3/2, self.dt**2, 0, 0], 
							[0, 0, self.dt**4/4 ,self.dt**3/2],
							[0, 0, self.dt**3/2,self.dt**2]])
		
		self.erroCov = self.P
		self.state = np.matrix([[0],[1],[0],[1]])


	"""Predict function which predicst next state based on previous state"""
	def predict(self):
		self.predictedState = self.A*self.state + self.B*self.U
		self.predictedErrorCov = self.A*self.erroCov*self.A.T + self.Q
		temp = np.asarray(self.predictedState)
		return temp[0], temp[2]

	"""Correct function which correct the states based on measurements"""
	def correct(self, currentMeasurement):
		self.kalmanGain = self.predictedErrorCov*self.H.T*np.linalg.pinv(
								self.H*self.predictedErrorCov*self.H.T+self.R)
		self.state = self.predictedState + self.kalmanGain*(currentMeasurement
											   - (self.H*self.predictedState))
		

		self.erroCov = (np.identity(self.P.shape[0]) - 
								self.kalmanGain*self.H)*self.predictedErrorCov



class Tracks(object):
	"""docstring for Tracks"""
	def __init__(self, detection, trackId):
		super(Tracks, self).__init__()
		self.KF = KalmanFilter()
		self.KF.predict()
		self.KF.correct(np.matrix(detection).reshape(2,1))
		self.trace = deque(maxlen=20)
		self.prediction = detection.reshape(1,2)
		self.trackId = trackId
		self.skipped_frames = 0

	def predict(self,detection):
		self.prediction = np.array(self.KF.predict()).reshape(1,2)
		self.KF.correct(np.matrix(detection).reshape(2,1))


class Tracker(object):
	"""docstring for Tracker"""
	def __init__(self, dist_threshold, max_frame_skipped, max_trace_length):
		super(Tracker, self).__init__()
		self.dist_threshold = dist_threshold
		self.max_frame_skipped = max_frame_skipped
		self.max_trace_length = max_trace_length
		self.trackId = 0
		self.tracks = []

	def update(self, detections):
		if len(self.tracks) == 0:
			for i in range(detections.shape[0]):
				track = Tracks(detections[i], self.trackId)
				self.trackId +=1
				self.tracks.append(track)

		N = len(self.tracks)
		M = len(detections)
		cost = []
		for i in range(N):
			diff = np.linalg.norm(self.tracks[i].prediction - detections.reshape(-1,2), axis=1)
			cost.append(diff)

		cost = np.array(cost)*0.1
		row, col = linear_sum_assignment(cost)
		assignment = [-1]*N
		for i in range(len(row)):
			assignment[row[i]] = col[i]

		un_assigned_tracks = []

		for i in range(len(assignment)):
			if assignment[i] != -1:
				if (cost[i][assignment[i]] > self.dist_threshold):
					assignment[i] = -1
					un_assigned_tracks.append(i)
				else:
					self.tracks[i].skipped_frames +=1

		del_tracks = []
		for i in range(len(self.tracks)):
			if self.tracks[i].skipped_frames > self.max_frame_skipped :
				del_tracks.append(i)

		if len(del_tracks) > 0:
			for i in range(len(del_tracks)):
				del self.tracks[i]
				del assignment[i]

		for i in range(len(detections)):
			if i not in assignment:
				track = Tracks(detections[i], self.trackId)
				self.trackId +=1
				self.tracks.append(track)


		for i in range(len(assignment)):
			if(assignment[i] != -1):
				self.tracks[i].skipped_frames = 0
				self.tracks[i].predict(detections[assignment[i]])
			self.tracks[i].trace.append(self.tracks[i].prediction)







		




