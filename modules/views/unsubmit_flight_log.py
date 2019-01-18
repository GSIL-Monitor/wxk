# -*- coding:utf-8 -*-

import time

from modules.models.flightlog.flightlog import FlightLog
from modules.flows.operations import Finish
from modules.perms import ActionNeedPermission
from modules.flows.states import Finished


def process_flight_log(log):
    date = log.flightDate
    return {
        'date': date.strftime("%Y-%m-%d"),
        'stamp': int(time.mktime(date.timetuple()))
    }


def get_flightlog_unsubmit(perm=False, max_number=5,
                           process=process_flight_log):

    if not perm:
        return []
    unsubmit_log = FlightLog.query.filter(
        FlightLog.status != Finished).group_by(
            FlightLog.flightDate).limit(max_number)
    return [process(item) for item in unsubmit_log]


def flight_log_notice(app):

    @app.context_processor
    def notice():
        perm = ActionNeedPermission('flightlog', Finish)
        can = perm.can()
        return {
            'flight_log_notices': get_flightlog_unsubmit(perm=can),
            'can_flight_notices': can,
        }
