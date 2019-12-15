
from my_utils import geometry
import math
import numpy as np
from shapely.geometry import Point
import time


def el_judge_12(human_keypoints, TableCali):


    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5] 
    MidHip = human_keypoints[8] 
    RHip = human_keypoints[9] 
    LHip = human_keypoints[12]
    Neck_MidHip = np.add((Neck-MidHip)/3.0*2, MidHip)
    human_rotate_position = 'front'
    RKnee = human_keypoints[10]

    main_ax = TableCali['long_axis']
    sub_ax = TableCali['short_axis']
    el_x = TableCali['x_center']
    el_y = TableCali['y_center']

    distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, math.degrees(TableCali['theta']))
    if geometry.is_in_ellipse_table(el_x,el_y,Neck[0], Neck[1], main_ax,sub_ax, TableCali['theta']) is False:
    # 计算人在桌子的哪个方向
        distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, math.degrees(TableCali['theta']))
        human2table_angle = geometry.get_angle([TableCali['back_x'], TableCali['back_y']], [el_x, el_y], [px, py])
    else:
        human2table_angle = 0

    check_1 = geometry.is_in_ellipse_table(el_x+30, el_y+60, RHip[0], RHip[1], 2.2*main_ax, 2.6*sub_ax, TableCali['theta'])
    check_2 = geometry.is_in_ellipse_table(el_x+30, el_y+60, LHip[0], LHip[1], 2.2*main_ax, 2.6*sub_ax, TableCali['theta'])
    
    if RKnee[2] > 0.4 and MidHip[2] > 0.4:
        angle_ll = geometry.get_angle([RKnee[0], RKnee[1]], [MidHip[0], MidHip[1]], [Neck[0], Neck[1]])
        print(angle_ll)
        if angle_ll > 155 :
            check_6 = False
        else:
            check_6 = True
    else :
        check_6 = True

    if human2table_angle <= 40:
        human_rotate_position = 'back'
        check_3 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0, sub_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0, sub_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0, sub_ax)

    elif human2table_angle <= 140:
        human_rotate_position = 'side'
        check_3 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, sub_ax, 1.5*main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, RShoulder, sub_ax, 2*main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, LShoulder, sub_ax, 2*main_ax)
    else :
        human_rotate_position = 'front'
        check_3 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0.8*sub_ax, main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0.8*sub_ax, main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0.8*sub_ax, main_ax)
    #print(human_rotate_position)
    #print(check_1,check_2,check_3,check_4, check_5, check_6, sep=' ')

    iNTable = check_1 and check_2 and check_3  and check_4 and check_5 and check_6

    return iNTable, Neck, human_rotate_position, distancetotable, px, py


def el_judge_13(human_keypoints, TableCali):
    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5] 
    MidHip = human_keypoints[8] 
    RHip = human_keypoints[9] 
    LHip = human_keypoints[12]
    Neck_MidHip = np.add((Neck-MidHip)/3.0*2, MidHip)
    human_rotate_position = 'front'
    RKnee = human_keypoints[10]

    main_ax = TableCali['long_axis']
    sub_ax = TableCali['short_axis']
    el_x = TableCali['x_center']
    el_y = TableCali['y_center']

    distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, math.degrees(TableCali['theta']))
    if geometry.is_in_ellipse_table(el_x,el_y,Neck[0], Neck[1], main_ax,sub_ax, TableCali['theta']) is False:
    # 计算人在桌子的哪个方向
        distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, math.degrees(TableCali['theta']))
        human2table_angle = geometry.get_angle([TableCali['back_x'], TableCali['back_y']], [el_x, el_y], [px, py])
    else:
        human2table_angle = 0

    check_1 = geometry.is_in_ellipse_table(el_x-20, el_y+95, RHip[0], RHip[1], 2.1*main_ax, 2.4*sub_ax, TableCali['theta'])
    check_2 = geometry.is_in_ellipse_table(el_x-20, el_y+95, RHip[0], RHip[1], 2.1*main_ax, 2.4*sub_ax, TableCali['theta'])
    
    if RKnee[2] > 0.4 and MidHip[2] > 0.4:
        angle_ll = geometry.get_angle([RKnee[0], RKnee[1]], [MidHip[0], MidHip[1]], [Neck[0], Neck[1]])
        #print(angle_ll)
        if angle_ll > 150 :
            check_6 = False
        else:
            check_6 = True
    else :
        check_6 = True

    if human2table_angle <= 40:
        human_rotate_position = 'back'
        check_3 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0, sub_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0, sub_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0, sub_ax)

    elif human2table_angle <= 140:
        human_rotate_position = 'side'
        check_3 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, sub_ax, 1.5*main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, RShoulder, sub_ax, 2*main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, LShoulder, sub_ax, 2*main_ax)
    else :
        human_rotate_position = 'front'
        check_3 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0.8*sub_ax, main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0.8*sub_ax, main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0.8*sub_ax, main_ax)
    #print(human_rotate_position)
    #print(check_1,check_2,check_3,check_4, check_5, check_6, sep=' ')

    iNTable = check_1 and check_2 and check_3  and check_4 and check_5 and check_6

    return iNTable, Neck, human_rotate_position, distancetotable, px, py

   

def el_judge_11(human_keypoints, TableCali):

    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5] 
    MidHip = human_keypoints[8] 
    RHip = human_keypoints[9] 
    LHip = human_keypoints[12]
    #RBigToe = human_keypoints[22]
    RKnee = human_keypoints[10]

    Neck_MidHip = np.add((Neck-MidHip)/3.0*2, MidHip)
    human_rotate_position = 'front'

    main_ax = TableCali['long_axis']
    sub_ax = TableCali['short_axis']
    el_x = TableCali['x_center']
    el_y = TableCali['y_center']

    distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, 180-math.degrees(TableCali['theta']))
    if geometry.is_in_ellipse_table(el_x,el_y,Neck[0], Neck[1], main_ax,sub_ax, TableCali['theta']) is False:
    # 计算人在桌子的哪个方向
        distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, 180-math.degrees(TableCali['theta']))
        human2table_angle = geometry.get_angle([TableCali['back_x'], TableCali['back_y']], [el_x, el_y], [px, py])
    else:
        human2table_angle = 0
    angle_shouders = geometry.get_angle([RShoulder[0], RShoulder[1]], [el_x, el_y], [LShoulder[0], LShoulder[1]])


    # 判断肩膀在不在 大椭圆内
    check_1 = geometry.is_in_ellipse_table(el_x,el_y-23,RShoulder[0], RShoulder[1], 2.7*main_ax,4.5*sub_ax, TableCali['theta'])
    check_2 = geometry.is_in_ellipse_table(el_x,el_y-23,LShoulder[0], LShoulder[1], 2.7*main_ax,4.5*sub_ax, TableCali['theta'])
    if RKnee[2] > 0.5 and MidHip[2] > 0.5:
        check_7 = False if geometry.get_angle([RKnee[0], RKnee[1]], [MidHip[0], MidHip[1]], [Neck[0], Neck[1]]) > 140 else True
    else :
        check_7 = True
    if human2table_angle <= 30:
        human_rotate_position = 'back'
        check_3 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0.3*sub_ax, 0.7*main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0.3*sub_ax, 0.7*main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0.7*sub_ax, 0.7*main_ax)
        check_6 = True if angle_shouders < 35 else False

    elif human2table_angle <= 120:
        human_rotate_position = 'side'
        if (check_1 and check_2) is True :
            check_1 = geometry.KeypointPositionCheck(TableCali, RShoulder, sub_ax, 1.3*main_ax)
            check_2 = geometry.KeypointPositionCheck(TableCali, LShoulder, sub_ax, 1.3*main_ax)
        check_3 = geometry.KeypointPositionCheck(TableCali, RHip, 0.7*sub_ax, main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, LHip, 0.7*sub_ax, main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0.8*sub_ax, main_ax)
        check_6 = True if angle_shouders < 35 else False

    else :
        human_rotate_position = 'front'
        # 肩膀在内测椭圆外
        # 肩膀的纵坐标 之差小于阈值
        check_3 = geometry.KeypointPositionCheck(TableCali, RShoulder, sub_ax, 1.1*main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, LShoulder, sub_ax, 1.1*main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, Neck_MidHip, 0.7*sub_ax, 0.8*main_ax)
        check_6 = True if angle_shouders < 50 else False
                                        
    #print(check_1,check_2,check_3,check_4, check_5, check_6, check_7, sep=' ')
    iNTable = check_1 and check_2 and check_3 and check_4 and check_5 and check_6 and check_7

    return iNTable, Neck, human_rotate_position, distancetotable, px, py

def el_judge_10(human_keypoints, TableCali):


    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5] 
    MidHip = human_keypoints[8] 
    #Neck_MidHip = np.add((Neck-MidHip)/3.0*2, MidHip)
    human_rotate_position = 'front'
    RKnee = human_keypoints[10]
    RHip = human_keypoints[9] 
    LHip = human_keypoints[12] 

    main_ax = TableCali['long_axis']
    sub_ax = TableCali['short_axis']
    el_x = TableCali['x_center']
    el_y = TableCali['y_center']

    #print(180-math.degrees(TableCali['theta']))
    distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, math.degrees(TableCali['theta']))
    if geometry.is_in_ellipse_table(el_x,el_y,Neck[0], Neck[1], main_ax,sub_ax, TableCali['theta']) is False:
    # 计算人在桌子的哪个方向
        distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1], main_ax, sub_ax, el_x, el_y, math.degrees(TableCali['theta']))
        human2table_angle = geometry.get_angle([TableCali['back_x'], TableCali['back_y']], [el_x, el_y], [px, py])
    else:
        human2table_angle = 0


    check_1 = geometry.is_in_ellipse_table(el_x, el_y, RShoulder[0], RShoulder[1], 3.2*main_ax, 4.2*sub_ax, TableCali['theta'])
    check_2 = geometry.is_in_ellipse_table(el_x, el_y, LShoulder[0], LShoulder[1], 3.2*main_ax, 4.2*sub_ax, TableCali['theta'])
    check_3 = geometry.is_in_ellipse_table(el_x, el_y, Neck[0], Neck[1], 3.2*main_ax, 4.2*sub_ax, TableCali['theta'])

    if RKnee[2] > 0.4 and MidHip[2] > 0.4:
        angle_ll = geometry.get_angle([RKnee[0], RKnee[1]], [MidHip[0], MidHip[1]], [Neck[0], Neck[1]])
        #print(angle_ll)
        if angle_ll > 140 :
            check_4 = False
        else:
            check_4 = True
    else :
        check_4 = True

    if human2table_angle <= 70:
        human_rotate_position = 'back'

        check_5 = geometry.is_Between2value(RShoulder[1], el_y-sub_ax, el_y+main_ax)
        check_6 = geometry.is_Between2value(LShoulder[1], el_y-sub_ax, el_y+main_ax)
        check_7 = geometry.is_Between2value(RShoulder[0], el_x-1.4*main_ax, el_x+1.4*main_ax)
        check_8 = geometry.is_Between2value(LShoulder[0], el_x-1.4*main_ax, el_x+1.4*main_ax)

        check_9 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0, 1.5*sub_ax)
        check_10 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0, 1.5*sub_ax)
        check_11 = geometry.KeypointPositionCheck(TableCali, Neck, 0, 1.5*sub_ax)

        check_8 = (check_11 and check_10 and check_9 and check_8)
    elif human2table_angle <= 105:
        human_rotate_position = 'side'

        check_5 = True
        check_6 = True
        if RHip[2] > 0.4:
            check_5 = geometry.KeypointPositionCheck(TableCali, RHip, 1.5*sub_ax, 1.3*main_ax)
        else :
            check_5 = True
        if LHip[2] > 0.4:
            check_6 = geometry.KeypointPositionCheck(TableCali, LHip, 1.5*sub_ax, 1.3*main_ax)
        else :
            check_6 = True

        check_7 = geometry.is_Between2value(RShoulder[1], el_y-1.6*main_ax, el_y+2*main_ax)
        check_8 = geometry.is_Between2value(LShoulder[1], el_y-1.6*main_ax, el_y+2*main_ax)

    else :
        human_rotate_position = 'front'
        check_5 = geometry.is_Between2value(RShoulder[1], el_y-2*main_ax, el_y-sub_ax)
        check_6 = geometry.is_Between2value(LShoulder[1], el_y-2*main_ax, el_y-sub_ax)
        check_7 = geometry.is_Between2value(RShoulder[0], el_x-1.8*main_ax, el_x+1.8*main_ax)
        check_8 = geometry.is_Between2value(LShoulder[0], el_x-1.8*main_ax, el_x+1.8*main_ax)

    #print(check_1, check_2, check_3, check_4, sep=' ')

    iNTable = (check_1 and check_2 and check_3 and check_4 and check_5 and check_6 and check_7 and check_8) 

    return iNTable, Neck, human_rotate_position, distancetotable, px, py



def el_judge_7(human_keypoints, TableCali):

    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5] 
    RHip = human_keypoints[9] 
    LHip = human_keypoints[12]
    human_rotate_position = 'front'

    main_ax = TableCali['long_axis']
    sub_ax = TableCali['short_axis']
    el_x = TableCali['x_center']
    el_y = TableCali['y_center']

    distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, 180-math.degrees(TableCali['theta']))
    if geometry.is_in_ellipse_table(el_x,el_y,Neck[0], Neck[1], main_ax,sub_ax, TableCali['theta']) is False:
    # 计算人在桌子的哪个方向
        distancetotable, px, py = geometry.estimate_distance(Neck[0], Neck[1],main_ax, sub_ax, el_x, el_y, 180-math.degrees(TableCali['theta']))
        human2table_angle = geometry.get_angle([TableCali['back_x'], TableCali['back_y']], [el_x, el_y], [px, py])
    else:
        human2table_angle = 0
    angle_shouders = geometry.get_angle([RShoulder[0], RShoulder[1]], [el_x, el_y], [LShoulder[0], LShoulder[1]])


    # 判断肩膀在不在 大椭圆内
    check_1 = geometry.is_in_ellipse_table(el_x,el_y,RShoulder[0], RShoulder[1], 2.5*main_ax,3.8*sub_ax, TableCali['theta'])
    check_2 = geometry.is_in_ellipse_table(el_x,el_y,LShoulder[0], LShoulder[1], 2.5*main_ax,3.8*sub_ax, TableCali['theta'])

    if human2table_angle <= 40:
        human_rotate_position = 'back'
        check_1 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0.7*sub_ax, 0.7*main_ax)
        check_2 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0.7*sub_ax, 0.7*main_ax)
        check_3 = geometry.is_Between2value(Neck[1], el_y+0.5*sub_ax, el_y + sub_ax + main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, LHip, 0.7*sub_ax, main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, Neck, 0.7*sub_ax, 0.7*main_ax)
        if angle_shouders > 50:
            check_1 = False
        if geometry.KeypointPositionCheck(TableCali, RHip, 0.7*sub_ax, main_ax) is False :
            check_1 = False
    elif human2table_angle <= 140:
        human_rotate_position = 'side'
        check_3 = geometry.KeypointPositionCheck(TableCali, RHip, 0.7*sub_ax, 0.8*main_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, LHip, 0.7*sub_ax, 0.8*main_ax)
        check_1 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0.7*sub_ax, 1.2*main_ax)
        check_2 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0.7*sub_ax, 1.2*main_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, Neck, sub_ax, main_ax)
        if angle_shouders > 40:
            check_1 = False
    else :
        human_rotate_position = 'front'
        check_3 = geometry.KeypointPositionCheck(TableCali, RHip, 0.5*sub_ax, 1.5*sub_ax)
        check_4 = geometry.KeypointPositionCheck(TableCali, LHip, 0.5*sub_ax, 1.5*sub_ax)
        check_1 = geometry.KeypointPositionCheck(TableCali, RShoulder, 0.8*sub_ax, 1.5*sub_ax)
        check_2 = geometry.KeypointPositionCheck(TableCali, LShoulder, 0.8*sub_ax, 1.5*sub_ax)
        check_5 = geometry.KeypointPositionCheck(TableCali, Neck, sub_ax, 0.8*main_ax)
        if angle_shouders > 45:
            check_1 = False
        if geometry.is_Between2value(RShoulder[1], el_y, el_y + 2.5*sub_ax) is False:
            check_1 = False
    check_6 = True 
                    
    iNTable = check_1 and check_2 and check_3 and check_4 and check_5 and check_6

    return iNTable, Neck, human_rotate_position, distancetotable, px, py



def sq_judge(human_keypoints, TableCali):

    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5]

    table_front = [(TableCali['front_top_left'][0], TableCali['front_top_left'][1]), (TableCali['front_top_right'][0], TableCali['front_top_right'][1]),
    (TableCali['front_bottom_right'][0], TableCali['front_bottom_right'][1]),(TableCali['front_bottom_left'][0], TableCali['front_bottom_left'][1])]

    table_back = [(TableCali['back_top_left'][0], TableCali['back_top_left'][1]), (TableCali['back_top_right'][0], TableCali['back_top_right'][1]),
    (TableCali['back_bottom_right'][0], TableCali['back_bottom_right'][1]),(TableCali['back_bottom_left'][0], TableCali['back_bottom_left'][1])]
    
    check_1 = geometry.is_in_square_table(table_front, Point(Neck[0], Neck[1]))
    check_2 = geometry.is_in_square_table(table_front, Point(RShoulder[0], RShoulder[1]))
    check_3 = geometry.is_in_square_table(table_front, Point(LShoulder[0], LShoulder[1]))

    iNTable = check_1 and check_2 and check_3

    if iNTable is True:
        return iNTable, Neck, human_keypoints

    check_1 = geometry.is_in_square_table(table_back, Point(Neck[0], Neck[1]))
    check_2 = geometry.is_in_square_table(table_back, Point(RShoulder[0], RShoulder[1]))
    check_3 = geometry.is_in_square_table(table_back, Point(LShoulder[0], LShoulder[1]))

    iNTable = check_1 and check_2 and check_3
    if iNTable is True:
        return iNTable, Neck, human_keypoints 
    
    return iNTable, Neck, human_keypoints

human_list_lenth = 10

def update_table_human_list(table_human_num, tableid, table_human_list):
    
    if len(table_human_list[tableid]) == human_list_lenth:
        del table_human_list[tableid][0]
        table_human_list[tableid].append(table_human_num)
    else:
        table_human_list[tableid].append(table_human_num)

def update_sqtable_human_fr(table_human_num, tableid, table_human_list):
    
    if len(table_human_list[tableid]['front']) == human_list_lenth:
        del table_human_list[tableid]['front'][0]
        table_human_list[tableid]['front'].append(table_human_num)
    else:
        table_human_list[tableid]['front'].append(table_human_num)

def update_sqtable_human_bk(table_human_num, tableid, table_human_list):
    
    if len(table_human_list[tableid]['back']) == human_list_lenth:
        del table_human_list[tableid]['back'][0]
        table_human_list[tableid]['back'].append(table_human_num)
    else:
        table_human_list[tableid]['back'].append(table_human_num)

def update_tablehumannum_db(table_human_number_list, tableid):
    curr_number_list = table_human_number_list[str(tableid)]
    if len(curr_number_list) == human_list_lenth:
        if curr_number_list[4] != curr_number_list[5]:
            if curr_number_list[5] == curr_number_list[6] == curr_number_list[7] ==curr_number_list[8] ==curr_number_list[9] :
                return True
            else: 
                return False
        else:
            return False
    else:
        return False 


def update_tablehumannum(table_human_number_list, tableid):
    curr_number_list = table_human_number_list[str(tableid)]
    if len(curr_number_list) == human_list_lenth:
        print(curr_number_list)
        if (curr_number_list[0] != curr_number_list[1]) and (curr_number_list.count(curr_number_list[9]) >= 7) :
            return True
        else: 
            return False
    else:
        return False



def sq_side_judge(human_keypoints, TableCali):

    Neck = human_keypoints[1]
    RShoulder = human_keypoints[2]
    LShoulder = human_keypoints[5]


    table_front = [(TableCali['front_top_left'][0], TableCali['front_top_left'][1]), (TableCali['front_top_right'][0], TableCali['front_top_right'][1]),
    (TableCali['front_bottom_right'][0], TableCali['front_bottom_right'][1]),(TableCali['front_bottom_left'][0], TableCali['front_bottom_left'][1])]

    table_back = [(TableCali['back_top_left'][0], TableCali['back_top_left'][1]), (TableCali['back_top_right'][0], TableCali['back_top_right'][1]),
    (TableCali['back_bottom_right'][0], TableCali['back_bottom_right'][1]),(TableCali['back_bottom_left'][0], TableCali['back_bottom_left'][1])]
    

    if table_front[0] != (0,0) :
        check_1 = geometry.is_in_square_table(table_front, Point(Neck[0], Neck[1]))
        check_2 = geometry.is_in_square_table(table_front, Point(RShoulder[0], RShoulder[1]))
        check_3 = geometry.is_in_square_table(table_front, Point(LShoulder[0], LShoulder[1]))
        iNTable = check_1 and check_2 and check_3
        return iNTable, Neck, 'front'

    else:

        check_1 = geometry.is_in_square_table(table_back, Point(Neck[0], Neck[1]))
        check_2 = geometry.is_in_square_table(table_back, Point(RShoulder[0], RShoulder[1]))
        check_3 = geometry.is_in_square_table(table_back, Point(LShoulder[0], LShoulder[1]))
        iNTable = check_1 and check_2 and check_3
        return iNTable, Neck, 'back'

