#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author: Sixzeroo
# website: www.liuin.cn

import json,hashlib

from hfut import Student

from config import STUDENT_ID, STUDENT_PASSWD

class Stu(object):
    def __init__(self, stu_id, std_pw):
        self.stu = Student(stu_id, std_pw, 'xc')

    @classmethod
    def sim_achi(cls, obj):
        b_key = obj['课程代码'] + obj['学期']
        m = hashlib.md5()
        m.update(b_key.encode('utf-8'))
        key = m.hexdigest()
        res = {
            'key': key,
            'course_name': obj['课程名称']
        }
        return res

    def get_achievement(self):
        b_achi = self.stu.get_my_achievements()
        res = [Stu.sim_achi(i) for i in b_achi]
        return res

if __name__ == '__main__':
    a = Stu()
    test = a.get_achievement()