# coding: utf-8

from __future__ import unicode_literals

from modules.flows.operations import Approved, ApproveRefuse


def reversed_cmp(x, y):
    if x == Approved and y == ApproveRefuse:
        return -1
    if y == Approved and x == ApproveRefuse:
        return 1
    return 0
