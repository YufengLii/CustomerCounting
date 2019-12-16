#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'werewolfLu'

import json
import uuid
from modules.baidutil import BAIDUFace, img_encodeb64
try:
    from modules.dbutil2 import DBPool as MySQLPlugin
except ImportError:
    from modules.dbutil import MySQLPlugin

from concurrent.futures import ThreadPoolExecutor, as_completed

# engine =BAIDUFace()
# db = MySQLPlugin()


GROUP = {
    'member': 'member1',
    'stranger': 'stranger'
}

QPS = 15


class FaceAPI(object):

    def __init__(self, engine=BAIDUFace(), db=MySQLPlugin()):
        super(FaceAPI, self).__init__()
        self.engine = engine
        self.db = db
        self.pool = ThreadPoolExecutor(max_workers=QPS)
        self.insert_stranger_ts = time.time()

    def detect(
            self,
            img,
            face_field=None):
        if face_field is None: face_field='age,gender,glasses,emotion,angel,feature'
        img_type = 'FACE_TOKEN' if type(img) == str and len(img) == 32 else "BASE64"
        img = img_encodeb64(img)

        return self.engine.face_detect(img, image_type=img_type, face_field=face_field)

    def __add_user(self, img, name=None, property=None, group=GROUP['stranger']):
        """ Add 1s delay between putting stranger into db to avoid multiply faces from single people """
        if group != GROUP['member'] and time.time() - self.insert_stranger_ts < 1: return -1

        img_type = 'FACE_TOKEN' if type(img) == str and len(img) == 32 else "BASE64"
        uid = str(uuid.uuid1()).replace('-', '')
        rt = self.engine.add_user(
            image=img_encodeb64(img), user_id=uid, user_name=name, image_type=img_type,
            group_id=group, action_type='APPEND')
        # print('userid', uid)

        if rt and rt.get('face_token'):
            if group == GROUP['member']:
                err = self.db.add_user(uid, name, group, 'default')
            else:
                err = self.db.add_stranger(uid, (name or "Unknown")+uid, property, group, 'default')
                self.insert_stranger_ts = time.time()

            if 0 != err:
                self.engine.del_user(uid, group)
        return uid

    def add_member(self, img, name):
        return self.__add_user(img, name, group=GROUP['member'])

    def add_stranger(self, img, property):
        return self.__add_user(img, name="Unknown", property=json.dumps(property), group=GROUP['stranger'])

    def identify(self, img, property=None):
        t1 = time.time()
        img_type = 'FACE_TOKEN' if type(img) == str and len(img) == 32 else "BASE64"
        img = img_encodeb64(img)
        gup = "{},{}".format(GROUP['member'], GROUP['stranger'])
        # gup = GROUP['stranger']
        rt = self.engine.face_identity(img, image_type=img_type, group_id_list=gup)
        if rt != -1 and rt.get('user_list') and property is not None:
            rt['user_list'][0].update(property)
        # else: print(123, property)
        print("identity:", time.time()-t1)
        return rt

    def identify_w_db(self, img, property=None):
        rt = self.identify(img)
        if rt != -1 and rt.get('user_list'):
            user = rt['user_list'][0]
            if user['score'] > 80:
                if property is not None:
                    user.update(property)
                return rt
            elif property is not None and property['face_probability'] > 0.8:
                uid = self.add_stranger(img, property)
                if uid != -1:
                    fake = {"group_id": GROUP["stranger"],
                             "user_id": uid,
                            "user_info": "Unknown"+uid,
                            "score": 100,
                            "new_stranger": True}
                    if property is not None:
                        fake.update(property)
                    return fake
        return -1

    def detect_and_identify(self, img, use_token=True, add_stranger=False):
        t1 = time.time()
        rt = self.detect(img)

        identify = self.identify_w_db if add_stranger else self.identify
        print("detect:", time.time()-t1)
        if rt != -1 and rt.get('face_list'):
            print("\n[INFO] headcount", len(rt['face_list']), '\n')

            if use_token is False:
                all_task = [self.pool.submit(identify,
                  img[int(face['location']['top']):int(face['location']['top'] + face['location']['height']),
                   int(face['location']['left']):int(face['location']['left'] + face['location']['width'])],
                                      face) for face in rt['face_list']]
            else:
                all_task = [self.pool.submit(identify, face['face_token'], face) for face in rt['face_list']]
            rst = []
            for future in as_completed(all_task):
                data = future.result()
                if data != -1 and data and data.get('user_list'):
                    rst.append(data)
            return rst


if __name__ == '__main__':
    import time
    import cv2
    from pprint import pprint

    face_api = FaceAPI()

    img = cv2.imread("/Users/ping/Downloads/group2.jpg")
    r = face_api.detect(img, face_field="age,gender,glass,emotion,angle,feature")
    pprint(r)
    rect = r['face_list'][0]['location']
    print(rect['top'], rect['top']+rect['height'], rect['left'], rect['left']+rect['width'])
    face = img[int(rect['top']):int(rect['top']+rect['height']), int(rect['left']):int(rect['left']+rect['width'])]

    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    # result, encimg = cv2.imencode('.jpg', face, encode_param)
    # open('/Users/ping/Downloads/aaa.jpeg', 'wb').write(encimg)


    while True:
        t1 = time.time()
        r = face_api.detect_and_identify(img, use_token=False, add_stranger=False)
        # pprint(r)
        if r:
            print([face['user_list'][0]['user_info'] for face in r])
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print(time.time() - t1)
        if time.time() - t1 > 0.5: print("===============================================")

    # face_api.add_member(face, "weizhi")
