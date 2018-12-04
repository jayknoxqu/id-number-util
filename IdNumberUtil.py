#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version 2.7.13

import datetime
import random
import re

# 导入区域编码
from area import addr

# 十五位身份证号表达式
ID_NUMBER_15_REGEX = '^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$'

# 十八位身份证号表达式
ID_NUMBER_18_REGEX = '^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'


class IdNumberUtil(object):

    def __init__(self, id_number):
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_area_name(self):
        """ 根据区域编号取出区域名称 """
        for area_info in addr:
            if area_info[0] == self.area_id:
                return area_info[1]
        else:
            return 'unknown'

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_sex(self):
        """ 通过身份证号获取性别， 女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @classmethod
    def verify_id(cls, id_number):
        """ 校验身份证是否正确 """
        if re.match(ID_NUMBER_18_REGEX, id_number):
            check_digit = cls(id_number).get_check_digit()
            return str(check_digit) == id_number[-1]
        else:
            return bool(re.match(ID_NUMBER_15_REGEX, id_number))

    @classmethod
    def generate_id(cls, sex=0):
        """
         随机生成身份证号，sex = 0表示女性，sex = 1表示男性
        """

        # 随机生成一个区域码(6位数)
        area_info = random.randint(0, len(addr))
        id_number = str(addr[area_info][0])

        # 限定出生日期范围(8位数)
        start, end = "1960-01-01", "2000-12-30"

        days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
        birth_days = datetime.datetime.strftime(
            datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d"
        )

        id_number += str(birth_days)
        # 顺序码(2位数)
        id_number += str(random.randint(10, 99))
        # 性别码(1位数)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码(1位数)
        return id_number + str(cls(id_number).get_check_digit())


if __name__ == '__main__':
    random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
    print IdNumberUtil.generate_id(random_sex)  # 随机生成身份证号
    print IdNumberUtil('410326199507103197').area_id  # 地址编码:410326
    print IdNumberUtil('410326199507103197').get_area_name()  # 地址:汝阳县
    print IdNumberUtil('410326199507103197').get_birthday()  # 生日:1995-7-10
    print IdNumberUtil('410326199507103197').get_age()  # 年龄:23(岁)
    print IdNumberUtil('410326199507103197').get_sex()  # 性别:1(男)
    print IdNumberUtil('410326199507103197').get_check_digit()  # 校验码:7
    print IdNumberUtil.verify_id('410326199507103198')  # 检验身份证是否正确:False
