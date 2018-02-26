# coding: utf-8

from __future__ import unicode_literals

from modules.forms.aircraft.aircraft import AircraftInformationForm
from .tranlate_column import column_labels


def Basic():
    return {
        '_api_url': '/v1/%(plane_type)saircraft/',
        # WUJG: 注意，当前所有飞机的格式是一样的，如果需要使用dict来分别
        # 区分不同的飞机模型实例，除此更改之外，需要在对应视图的create_view
        # 和edit_view相应的处理
        'form': AircraftInformationForm,
        'title': '基本信息',
        'coll_name': 'aircraft_information',
        'template': 'aircraft/basic.html',
        'column_list': [
            'sn', 'importedDate', 'manufacturer', 'acn',
            'sln', 'nrn', 'manufactureDate', 'permanentAirport',
            'flightTime', 'landTimes', 'remark', 'imageUrl',
            'engineNumber', 'acnDeadline', 'slnDeadline', 'nrnDeadline',
        ],
        'column_labels': column_labels,
        'details_columns': [
            'sn', 'importedDate', 'manufacturer', 'acn',
            'sln', 'nrn', 'manufactureDate', 'permanentAirport',
            'flightTime', 'landTimes', 'remark', 'imageUrl',
            'engineNumber', 'acnDeadline', 'slnDeadline', 'nrnDeadline',
        ],
    }
