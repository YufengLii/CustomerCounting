
# openpose config
params = dict()
params["model_folder"] = "/home/feng/Documents/openpose/models/"
params["model_pose"] = "BODY_25"
params["net_resolution"] = "-1x256"
params["num_gpu"] = 1
params["num_gpu_start"] = 0
op_params = params

oPPython = '/home/feng/Documents/openpose/build/python' 
# Video source
frame_url = './demo_videos/124_3.mp4'
# frame_url = 'rtsp://admin:helab401@192.168.31.124/Streaming/Channels/101'
requesturl = "http://192.168.31.33:3001/api/v1/sense/cv/customers/count"

# canteen human num init
canteen_human_num_init = 0
enter_num_init = 0
depart_num_init = 0

# calibration area
line_x_min = 150
line_x_max = 270
line_y_max = 1279
line_y_min = 1

area_id = 0