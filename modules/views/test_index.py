# coding: utf-8

import unittest
from jinja2 import Markup
from .index import list_level_compare_max


class MyTestCase(unittest.TestCase):

    def test_shortlist(self):
        show_list = []
        dict1 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {0: 20, 9: 15, 2: 23},
        }
        dict2 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {0: 20, 9: 15, 2: 23},
        }
        dict3 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {2: 23},
        }
        dict4 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {0: 18, 9: 15, 2: 23},
        }
        dict5 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {0: 15, 9: 15, 2: 23},
        }
        dict6 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {9: 12, 2: 23},
        }
        dict7 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {9: 8, 2: 23},
        }
        show_list.append(dict1)
        show_list.append(dict2)
        show_list.append(dict3)
        show_list.append(dict4)
        show_list.append(dict5)
        show_list.append(dict6)
        show_list.append(dict7)
        show_list.sort(list_level_compare_max)
        self.assertEqual(show_list[0], dict1, 'failed 1')
        self.assertEqual(show_list[1], dict5, 'failed 2')
        self.assertEqual(show_list[2], dict2, 'failed 3')
        self.assertEqual(show_list[3], dict7, 'failed 4')
        self.assertEqual(show_list[4], dict6, 'failed 5')
        self.assertEqual(show_list[5], dict3, 'failed 6')
        self.assertEqual(show_list[6], dict4, 'failed 7')

        dict2 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {0: 20, 9: 15},
        }
        dict1 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {0: 18, 9: 15, 2: 23},
        }
        dict4 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {9: 15, 2: 23},
        }
        dict3 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {9: 10, 2: 23},
        }
        dict6 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {2: 23},
        }
        dict5 = {
            'level': Markup('3级预警'.decode("utf-8")),
            'intervaltype': {3: 12},
        }
        dict8 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {2: 23},
        }
        dict7 = {
            'level': Markup('2级预警'.decode("utf-8")),
            'intervaltype': {0: 15},
        }
        dict9 = {
            'level': Markup('1级预警'.decode("utf-8")),
            'intervaltype': {9: 12, 2: 23},
        }
        dict10 = {
            'level': Markup('1级预警'.decode("utf-8")),
            'intervaltype': {2: 23},
        }
        dict11 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {0: 18, 9: 15, 2: 23},
        }

        dict12 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {0: 20},
        }
        dict13 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {9: 8, 2: 23},
        }
        dict14 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {9: 10, 2: 23},
        }
        dict15 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {2: 23},
        }
        dict16 = {
            'level': Markup('正常'.decode("utf-8")),
            'intervaltype': {4: 33},
        }
        show_list1 = []
        show_list1.append(dict11)
        show_list1.append(dict12)
        show_list1.append(dict13)
        show_list1.append(dict14)
        show_list1.append(dict15)
        show_list1.append(dict16)
        show_list1.append(dict7)
        show_list1.append(dict2)
        show_list1.append(dict3)
        show_list1.append(dict5)
        show_list1.append(dict6)
        show_list1.append(dict8)
        show_list1.append(dict4)
        show_list1.append(dict9)
        show_list1.append(dict10)
        show_list1.append(dict1)
        show_list1.sort(list_level_compare_max)
        self.assertEqual(show_list1[0], dict1, 'failed 11')
        self.assertEqual(show_list1[1], dict2, 'failed 12')
        self.assertEqual(show_list1[2], dict3, 'failed 13')
        self.assertEqual(show_list1[3], dict4, 'failed 14')
        self.assertEqual(show_list1[4], dict5, 'failed 15')
        self.assertEqual(show_list1[5], dict6, 'failed 16')
        self.assertEqual(show_list1[6], dict7, 'failed 17')
        self.assertEqual(show_list1[7], dict8, 'failed 18')
        self.assertEqual(show_list1[8], dict9, 'failed 19')
        self.assertEqual(show_list1[9], dict10, 'failed 110')
        self.assertEqual(show_list1[10], dict11, 'failed 111')
        self.assertEqual(show_list1[11], dict12, 'failed 112')
        self.assertEqual(show_list1[12], dict13, 'failed 113')
        self.assertEqual(show_list1[13], dict14, 'failed 114')
        self.assertEqual(show_list1[14], dict15, 'failed 115')
        self.assertEqual(show_list1[15], dict16, 'failed 116')
