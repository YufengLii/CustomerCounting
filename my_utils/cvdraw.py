import cv2
import math
def draw_rect(img, pt1, pt2, pt3, pt4):
    point_color = (0, 255, 0)  # BGR
    thickness = 4
    lineType = 4
    pt1 = ((int)(pt1[0]), (int)(pt1[1]))
    pt2 = ((int)(pt2[0]), (int)(pt2[1]))
    pt3 = ((int)(pt3[0]), (int)(pt3[1]))
    pt4 = ((int)(pt4[0]), (int)(pt4[1]))

    cv2.line(img, pt1, pt2, point_color, thickness, lineType)
    cv2.line(img, pt2, pt3, point_color, thickness, lineType)
    cv2.line(img, pt3, pt4, point_color, thickness, lineType)
    cv2.line(img, pt4, pt1, point_color, thickness, lineType)
    return img

def draw_table_info(image, camera_info):

    camera_table_calibration_info = camera_info['calibrations']
    for table_info in camera_table_calibration_info:
        if table_info['shape'] is 'ellipses':

            # ellipse_table_y_edge_min = (int)(table_info['y_center'] - table_info['short_axis'])
            # ellipse_table_y_edge_max = (int)(table_info['y_center'] + table_info['short_axis'])
            # ellipse_table_x_edge_min = (int)(table_info['x_center'] - table_info['long_axis'])
            # ellipse_table_x_edge_max = (int)(table_info['x_center'] + table_info['long_axis'])

            #cv2.line(image, (1, ellipse_table_y_edge_min), (2559, ellipse_table_y_edge_min), (255, 0, 0), 4, 4)
            #cv2.line(image, (1, ellipse_table_y_edge_max), (2559, ellipse_table_y_edge_max), (255, 0, 0), 4, 4)
            #cv2.line(image, (ellipse_table_x_edge_min, 1), (ellipse_table_x_edge_min, 1439), (255, 0, 0), 4, 4)
            #cv2.line(image, (ellipse_table_x_edge_max, 1), (ellipse_table_x_edge_max, 1439), (255, 0, 0), 4, 4)
            #cv2.line(image, (200, 300), ((int)(200+table_info['short_axis']),300), (0, 255, 0), 4, 4)
            #cv2.line(image, (200, 500), ((int)(200+table_info['long_axis']),500), (0, 255, 0), 4, 4)

            #cv2.ellipse(image, ((int)(table_info['x_center']), (int)(table_info['y_center'])),(int(0.8*table_info['long_axis']), int(0.8*table_info['short_axis'])), math.degrees(table_info['theta']), 0, 360,  (0, 255,0 ), 3)
            cv2.ellipse(image, ((int)(table_info['x_center']), (int)(table_info['y_center'])), (int(table_info['long_axis']), int(table_info['short_axis'])), math.degrees(table_info['theta']), 0, 360,  (0, 255, 0), 3)
            cv2.putText(image, "Table "+(str)(table_info['tableID']), ((int)(table_info['x_center']), (int)(table_info['y_center'])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            #print(table_info['center'][0])
            #print(table_info['center'][1])
            cv2.putText(image, "Table "+(str)(table_info['tableID']), ((int)(table_info['center'][0]), (int)(table_info['center'][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            draw_rect(image, tuple(table_info['top_left']), tuple(table_info['top_right']),tuple(table_info['bottom_right']),tuple(table_info['bottom_left']))
            draw_rect(image, tuple(table_info['back_top_left']), tuple(table_info['back_top_right']), tuple(table_info['back_bottom_right']),tuple(table_info['back_bottom_left']))
            draw_rect(image, tuple(table_info['front_top_left']), tuple(table_info['front_top_right']), tuple(table_info['front_bottom_right']),tuple(table_info['front_bottom_left']))
            #draw_rect(image,)
            #print('draw rectangle')
    return image


def draw_calibration_info(image, curr_camera_calibration_info):

    for table_info in curr_camera_calibration_info:
        if table_info['shape'] == 'ellipses':

            # ellipse_table_y_edge_min = (int)(table_info['y_center'] - table_info['short_axis'])
            # ellipse_table_y_edge_max = (int)(table_info['y_center'] + table_info['short_axis'])
            # ellipse_table_x_edge_min = (int)(table_info['x_center'] - table_info['long_axis'])
            # ellipse_table_x_edge_max = (int)(table_info['x_center'] + table_info['long_axis'])

            #cv2.line(image, (1, ellipse_table_y_edge_min), (2559, ellipse_table_y_edge_min), (255, 0, 0), 4, 4)
            #cv2.line(image, (1, ellipse_table_y_edge_max), (2559, ellipse_table_y_edge_max), (255, 0, 0), 4, 4)
            #cv2.line(image, (ellipse_table_x_edge_min, 1), (ellipse_table_x_edge_min, 1439), (255, 0, 0), 4, 4)
            #cv2.line(image, (ellipse_table_x_edge_max, 1), (ellipse_table_x_edge_max, 1439), (255, 0, 0), 4, 4)
            #cv2.line(image, (200, 300), ((int)(200+table_info['short_axis']),300), (0, 255, 0), 4, 4)
            #cv2.line(image, (200, 500), ((int)(200+table_info['long_axis']),500), (0, 255, 0), 4, 4)

            #cv2.ellipse(image, ((int)(table_info['x_center']-20), (int)(table_info['y_center']+95)),(int(2.1*table_info['long_axis']), int(2.4*table_info['short_axis'])), math.degrees(table_info['theta']), 0, 360,  (0, 255,0 ), 3)
            cv2.ellipse(image, ((int)(table_info['x_center']), (int)(table_info['y_center'])), (int(table_info['long_axis']), int(table_info['short_axis'])), math.degrees(table_info['theta']), 0, 360,  (0, 255, 0), 3)
            cv2.putText(image, "Table "+(str)(table_info['tableID']), ((int)(table_info['x_center']), (int)(table_info['y_center'])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:

            #print(table_info['center'][0])
            #print(table_info['center'][1])
            cv2.putText(image, "Table " +(str)(table_info['tableID']), ((int)(table_info['center'][0]), (int)(table_info['center'][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            draw_rect(image, tuple(table_info['top_left']), tuple(table_info['top_right']),tuple(table_info['bottom_right']),tuple(table_info['bottom_left']))
            draw_rect(image, tuple(table_info['back_top_left']), tuple(table_info['back_top_right']), tuple(table_info['back_bottom_right']),tuple(table_info['back_bottom_left']))
            draw_rect(image, tuple(table_info['front_top_left']), tuple(table_info['front_top_right']), tuple(table_info['front_bottom_right']),tuple(table_info['front_bottom_left']))
            #draw_rect(image,)
            #print('draw rectangle')
    return image

def RotateClockWise90(img):
    trans_img = cv2.transpose( img )
    new_img = cv2.flip(trans_img, 1)
    return new_img

def RotateAntiClockWise90(img):
    trans_img = cv2.transpose( img )
    new_img = cv2.flip( trans_img, 0 )
    return new_img

def image_preprocess(image, camera_info):
    #print(camera_info)
    cropped = image[camera_info[1]:camera_info[3],camera_info[0]:camera_info[2]]
    if camera_info[4] == 90:
        new_image = RotateClockWise90(cropped)
    elif camera_info[4] == -90:
        new_image = RotateAntiClockWise90(cropped)
    else:
        new_image = cropped
    return new_image



